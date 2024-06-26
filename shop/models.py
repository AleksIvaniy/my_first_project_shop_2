import uuid

from django.contrib.auth.models import User
from django.db import models
from datetime import datetime, date


# Create your models here.

# class Order(models.Model):
#     product = models.ForeignKey('Product', on_delete=models.CASCADE)
#     datetime = models.DateTimeField(null=True)
#     status = models.CharField(max_length=100)


class Category(models.Model):
    # id = # Django сам создает в каждой таблице поле id(pk) - SERIAL PK

    name = models.CharField(max_length=100)  # VARCHAR(100)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    VIN = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='products')
    price = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE, null=True)
    color = models.ForeignKey('Color', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.name} - {self.VIN}"


# class Customers(models.Model):
#     name = models.CharField(max_length=50)
#     surname = models.CharField(max_length=50)
#     tel = models.CharField(max_length=12)
#     iin = models.CharField(max_length=12)
#
#     def __str__(self):
#         return f"{self.status}"

class Cart(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.id)


class CartItems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, blank=True, null=True, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=0)


class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='rating')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    rating = models.PositiveIntegerField(
        choices=((1, '1 star'), (2, '2 star'), (3, '3 star'), (4, '4 star'), (5, '5 star')))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'user')

    def __str__(self):
        return f"{self.user}'s {self.rating}-star rating for {self.product}"


class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'

    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed'),
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    pending_status = models.CharField(
        max_length=50, choices=PAYMENT_STATUS_CHOICES, default='PAYMENT_STATUS_PENDING')
    owner = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.pending_status


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.product.name



