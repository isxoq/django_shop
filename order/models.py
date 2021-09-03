from django.db import models
from catalog.models import Product
from django.contrib.auth.models import User


# Create your models here.

class Cart(models.Model):
    product_id = models.ForeignKey(Product, models.CASCADE, 'cart_to_product_fk')
    quantity = models.IntegerField()
    user_id = models.ForeignKey(User, models.CASCADE, 'user_to_cart_fk')


class Order(models.Model):
    user_id = models.ForeignKey(User, models.CASCADE, 'user_to_order_fk')
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20)
    amount = models.IntegerField()
    state = models.IntegerField(choices=[
        (1, 'Tolov kutilmoqda'),
        (2, 'Tolov bajarildi'),
        (3, 'Bekor qilindi'),
        (4, 'Tugatildi'),
    ], default=1)


class OrderProduct(models.Model):
    order_id = models.ForeignKey(Order, models.CASCADE, 'order_product_to_product_fk')
    product_id = models.ForeignKey(Product, models.CASCADE, 'order_product_to_product_fk')
    quantity = models.IntegerField()
