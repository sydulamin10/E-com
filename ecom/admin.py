from django.contrib import admin
from .models import *

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id','user','auth_token','is_verified','credited_at']

class OrderPlacedAdmin(admin.ModelAdmin):
    list_display = ['id','user','customer','product','quantity','ordered_date']

class CartAdminModel(admin.ModelAdmin):
    list_display = ['id','user','product','quantity']


admin.site.register(Profile,ProfileAdmin)
admin.site.register(Product)
admin.site.register(OrderPlaced,OrderPlacedAdmin)
admin.site.register(Cart)
