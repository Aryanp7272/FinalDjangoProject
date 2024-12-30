from django.contrib import admin
from filmapp.models import Film,Plans

# Register your models here.
#admin.site.register(Product)

class FilmAdmin(admin.ModelAdmin):
    list_display=['id','name','price','type','language','country','time','is_active','image','is_paid','video','views']
    list_filter=['is_active','type','language','country','is_paid']
    
admin.site.register(Film,FilmAdmin)

class PalnAdmin(admin.ModelAdmin):
    list_display=['name','duration','charges']

admin.site.register(Plans,PalnAdmin)