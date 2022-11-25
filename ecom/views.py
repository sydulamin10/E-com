from django.shortcuts import render, redirect, reverse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import login, logout, authenticate
from django.views import View
from django.db.models import Q
from django.http import JsonResponse


def base(request):
    return render(request, 'app/base.html')


def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            username = user.username
            return render(request, 'ecom/store.html', {'fname': username})
        else:
            messages.error(request, "Bad creation")
            return redirect('app/base.html')

    return render(request, 'app/login.html')


def registration(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('pass')

        if User.objects.filter(username=username).first():
            messages.success(request, 'username already b  exists! please try some other name  ')
            return redirect('registration')
        if User.objects.filter(email=email).first():
            messages.success(request, 'email already register')
            return redirect('registration')
        user_obj = User.objects.create_user(username, email, password)
        user_obj.set_password(password)
        auth_token = str(uuid.uuid4())

        pro_obj = Profile.objects.create(user=user_obj, auth_token=auth_token)
        pro_obj.save()
        send_mail_registration(email, auth_token)
        return render(request, 'app/success.html')

    return render(request, 'app/registration.html')


def success(request):
    return render(request, 'app/success.html')


def token_send(request):
    return render(request, 'app/token_send.html')


def error(request):
    return render(request, 'app/error.html')


def send_mail_registration(email, token):
    subject = "your account need to verify"
    message = f'hi click the link for verify http://127.0.0.1:8000/account-verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)


def verify(request, auth_token):
    profile_obj = Profile.objects.filter(auth_token=auth_token).first()
    profile_obj.is_verified = True
    profile_obj.save()
    messages.success(request, 'OWWO,your mail is verified')
    print(auth_token)
    return redirect('login')


def signout(request):
    logout(request)
    return redirect('login')


def ProductDetails(request, pk):
    totalitem = 0
    product = Product.objects.get(pk=pk)
    item_already_in_cart = False
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()

    context = {
        'product': product,
        'totalitem': totalitem,
        'item_already_in_cart': item_already_in_cart,
    }
    return render(request, 'ecom/productdetails.html', context)


def store(request):
    totalitem = 0
    top = Product.objects.filter(category='T')
    bottom = Product.objects.filter(category='B')
    mobile = Product.objects.filter(category='M')
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))

    context = {
        'top': top,
        'bottom': bottom,
        'mobile': mobile,
        'totalitem': totalitem,

    }
    return render(request, 'ecom/store.html', context)


def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return render(request, 'ecom/store.html')


def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        # print(cart)
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        # print(cart_product)
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discount_price)
                amount += tempamount
                totalamount = amount + shipping_amount
            return render(request, 'ecom/cart.html', {'cart': cart, 'totalamount': totalamount, 'amount': amount})
        else:
            return render(request, 'ecom/store.html')


def pluscart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        # print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        # print(cart_product)
        for p in cart_product:
            tempamount = (p.quantity * p.product.discount_price)
            amount += tempamount
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount,
        }
        return JsonResponse(data)


def minuscart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        # print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discount_price)
            amount += tempamount
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount,
        }
        return JsonResponse(data)


def removecart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        # print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        # print(cart_product)

        for p in cart_product:
            tempamount = (p.quantity * p.product.discount_price)
            amount += tempamount

        data = {
            'amount': amount,
            'totalamount': amount + shipping_amount,

        }
        return JsonResponse(data)


def main(request):
    return render(request, 'ecom/main.html')
