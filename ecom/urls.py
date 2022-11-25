from django.contrib import admin
from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('base/',views.base,name='base'),

    #login system
    path('',views.Login,name='login'),
    path('registration/',views.registration,name='registration'),
    path('success/',views.success,name='success'),
    path('token/',views.token_send,name='token'),
    path('error/',views.error,name='error'),
    path('account-verify/<slug:auth_token>',views.verify,name='verify'),
    path('store/',views.store,name='store'),
    path('logout/',views.signout,name='logout'),

    #product details
    path('productdetails/<pk>',views.ProductDetails,name='productdetails'),
    path('show_cart/',views.show_cart,name="show_cart"),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('pluscart/',views.pluscart,name='pluscart'),
    path('minuscart/',views.minuscart,name='minuscart'),
    path('removecart/',views.removecart,name='removecart'),
    path('main/',views.main,name='main')

] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
