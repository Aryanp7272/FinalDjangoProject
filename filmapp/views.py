from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q
from django.contrib.auth.models import User
from filmapp.models import Film,Cart,Plans,FilmHistory,Subscriptions
import razorpay
from django.core.mail import send_mail
from django.utils.timezone import now
from datetime import timedelta
import re


# Create your views here.
def ulogin(request):
    context={}
    if request.method=='GET':
        return render(request,'login.html')
    else:
        
        n= request.POST['username']
        p= request.POST['password']
        
        e= authenticate(password=p,username=n)
        print(e)
        if e is not None:
            login(request,e)
            return redirect('/home')
        else:
            context['ermsg']='Invalid Username or Password'
            return render(request,'login.html',context)

def register(request):
    context={}
    if request.method =='GET':
        return render(request,'register.html')
    else:
        un=request.POST['username']
        ue=request.POST['useremail']
        p=request.POST['password']
        cp=request.POST['cpassword']
        """print(un)
        print(ue)
        print(p)
        print(cp)"""
        if un==''or ue=='' or p == '' or cp =='':
            
            context['ermsg']="all fields required"
            return render(request,'register.html',context)
        elif User.objects.filter(username=un).exists():
            
            context['ermsg'] = "Username already exists."
            return render(request, 'register.html', context)
        
        # elif not re.match(r'^[\w]+$', un):  
        #     context['ermsg'] = "Username should not contain special characters."
        #     return render(request, 'register.html', context)
        # elif p!=cp:

            context['ermsg']="Password does not match"
            return render(request,'register.html',context)
        elif len(p)<8:
            
            context['ermsg']="password must be of minimum 8 characters"
            return render(request,'register.html',context)
        
        else:
            u=User.objects.create(username=un,email=ue)
            u.set_password(p)
            u.save()
            context['success']="User registered successfully...!"
            return render(request,'register.html',context)
        


def about(request):
    return render(request,'about.html')

def home(request):
    f=Film.objects.filter(is_active=True)
    context={}
    print(f)
    context['data']=f
    return render(request,'index.html',context)

def info(request,fid):
    #print(fid)
    context={}
    f=Film.objects.filter(id=fid)
    context['data']=f
    return render(request,'info.html',context)

def user_logout(request):
    logout(request)
    return redirect('/home')

def addtocart(request,fid): 
    if request.user.is_authenticated:
        #print('user is logged in')
        u=User.objects.filter(id=request.user.id)
        p=Film.objects.filter(id=fid)
        context={}
        context['data']=p  
        q1=Q(uid=u[0])
        q2=Q(fid=p[0])
        c=Cart.objects.filter(q1 & q2)
        n=len(c)
        if n==0:
            c=Cart.objects.create(uid=u[0],fid=p[0])
            c.save()
            context['success']='Film added successfully to watchlist....!'
        else:
            context['ermsg']='Film already exists in watchlist...!'
        return render(request,'info.html',context)

    else:
        return redirect('/ulogin') 
    
def watchlist(request):
    f=Cart.objects.filter(uid=request.user.id)
    context={}
    if len(f) > 0:
        context['data']=f
    else:
        context['ermsg']='no movies in watchlist'
    return render(request,'watchlist.html',context)



def remove(request,cid):
    c=Cart.objects.filter(fid=cid)
    c.delete()
    a=Cart.objects.filter(uid=request.user.id)
    context={}
    context['data']=a
    return render(request,'watchlist.html',context)


def subscribe(request):
    if request.user.is_authenticated:
        p=Plans.objects.all()
        context={}
        context['data']=p
    else:
        return redirect('/ulogin')
    return render(request,'subscribe.html',context)


def buy(request,cid):
    c=Plans.objects.filter(id=cid)
    u=User.objects.filter(id=request.user.id)
    context={}
    context['data']=c
    context['user']=u
    return render(request,'placeorder.html',context)


def makepayment(request, n):
    client = razorpay.Client(auth=("rzp_test_CbepQPSX6Lp3CN", "dk1YgCyVZRSVoUT1OGNgjWC0"))
    user = request.user
    if not user.is_authenticated:
        return redirect('/ulogin')

    plan = Plans.objects.filter(name=n).first()
    if not plan:
        return redirect('/subscribe')

    Subscriptions.objects.create(
        pid=plan,
        uid=user,
        start_date=now(),
        end_date=now().date() + timedelta(days=30)
    )

    # Razorpay payment logic
    amount = plan.charges * 100
    data = {"amount": amount, "currency": "INR", "receipt": "order_rcptid_11"}
    payment = client.order.create(data=data)

    context = {"payment": payment}
    return render(request, 'pay.html', context)



def search(request):
    s=request.GET['search']
    fname=Film.objects.filter(name__icontains=s)
    ftype=Film.objects.filter(type__icontains=s)
    flang=Film.objects.filter(language__icontains=s)
    fcont=Film.objects.filter(country__icontains=s)
    allprod=ftype.union(fname,flang,fcont)
    context={}

    if allprod.count()==0:
        context['errmsg']='Film not Found...!'
  
    context['data']=allprod
    return render(request,'index.html',context)

def unpaid(request):
    u=Film.objects.filter(price=0)
    context={}
    context['data']=u
    return render(request,'index.html',context)


def paid(request):
    context={}
    p=Film.objects.filter(price__gt=0)
    #print(p)
    #p=Film.objects.filter(price>0)
    context['data']=p
    return render(request,'index.html',context)

def history(request, fid):
    context = {}
    user = request.user
    if not user.is_authenticated:
        return redirect('/ulogin')

    f = Film.objects.filter(id=fid).first()
    if not f:
        context['ermsg'] = 'Film not found.'
        return render(request, 'index.html', context)

    if f.is_paid:
        if not is_subscription_valid(user):
            context['ermsg'] = 'Your subscription has expired. Please subscribe to view paid content.'
            return render(request, 'index.html', context)

    # Increment views and add to history
    f.views += 1
    f.save()
    FilmHistory.objects.create(fid=f, uid=user)

    context['data'] = f
    return render(request, 'watch.html', context)


def viewhistory(request):
    h=FilmHistory.objects.filter(uid=request.user.id).order_by('-id')
    #print(h)
    context={}
    context['data']=h
    return render(request,'history.html',context)


def latest(request):
    context={}
    l=Film.objects.order_by('-id').all()[:5]
    context['data']=l
    return render(request,'index.html',context)

def catfilter(request,c):
    #print(c)
    context={}
    if c == "1":
        o=Film.objects.filter(type='Movie')
        #print(o)
    elif c == "2":
        o=Film.objects.filter(type='Web-Series')
    elif c == "3":
        o=Film.objects.filter(type='Drama')
    elif c == "4":
        o=Film.objects.filter(country='India')
    elif c == "5":
        o=Film.objects.filter(country='America')
    elif c == "6":
        o=Film.objects.filter(country='Korea')
    elif c == "7":
        o=Film.objects.filter(language='English')
    elif c == "8":
        o=Film.objects.filter(language='Hindi')
    else:
        o=Film.objects.filter(language='Chinese')

    context['data']=o
    return render(request,'index.html',context)


def paymentsuccess(request):
    u = User.objects.filter(id=request.user.id).first()
    subscription = Subscriptions.objects.filter(uid=u).order_by('-start_date').first()

    if subscription:
        end_date = subscription.end_date  
    else:
        end_date = now().date() + timedelta(days=30) 

   
    to = u.email
    sub = 'Film Site Subscription Confirmation'
    msg = f'Thank you for subscribing! Your subscription is valid until {end_date}.'
    frm = 'aryanpote2@gmail.com'

    # Send the email
    send_mail(
        sub, 
        msg, 
        frm, 
        [to], 
        fail_silently=False
    )

    return render(request, 'paymentsuccess.html')


def popular(request):
    p=Film.objects.order_by('-views').filter(is_active=True)[:10]
    context={}
    context['data']=p
    return render(request,'index.html',context)

def subscriptions(request):
    u=User.objects.filter(id=request.user.id)[0]
    s=Subscriptions.objects.filter(uid=u)
    context={}
    context['data']=s
    return render(request,'subscribers.html',context)

def is_subscription_valid(user):
    subscription = Subscriptions.objects.filter(uid=user).order_by('-start_date').first()
    if subscription and subscription.end_date > now().date():  
        return True
    return False