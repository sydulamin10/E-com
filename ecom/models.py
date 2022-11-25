from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    credited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    # def get_cart_count(self):
    #     return Cart.objects.filter(cart__is_paid=False, cart__user=self.user).count()


CATEGORY_PRODUCT = (
    ('T', 'Topwear'),
    ('B', 'Bottomwear'),
    ('E', 'Elctronic'),
    ('M', 'Mobile'),

)


class Product(models.Model):
    name = models.CharField(max_length=100)
    product_image = models.ImageField(upload_to='product')
    category = models.CharField(choices=CATEGORY_PRODUCT, max_length=5, null=True)
    price = models.PositiveIntegerField()
    discount_price = models.PositiveIntegerField()
    description = models.TextField(null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)


class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=1)
