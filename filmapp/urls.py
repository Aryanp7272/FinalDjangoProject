from django.urls import path
from filmapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('ulogin',views.ulogin),
    path('register',views.register),
    path('about',views.about),
    path('home',views.home),
    path('info/<fid>',views.info),
    path('logout',views.user_logout),
    path('addtowatchlist/<fid>',views.addtocart),
    path('watchlist',views.watchlist),
    path('remove/<cid>',views.remove),
    path('subscribe',views.subscribe),
    path('buy/<cid>',views.buy),
    path('makepayment/<n>',views.makepayment),
    path('search',views.search),
    path('unpaid',views.unpaid),
    path('paid',views.paid),
    path('history/<fid>',views.history),
    path('viewhistory',views.viewhistory),
    path('latest',views.latest),
    path('catfilter/<c>',views.catfilter),
    path('paymentsuccess',views.paymentsuccess),
    path('popular',views.popular),
    path('subscribtions',views.subscriptions),

]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)