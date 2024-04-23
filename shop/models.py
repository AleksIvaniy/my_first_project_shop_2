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
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)
    color = models.ForeignKey('Color', on_delete=models.CASCADE)

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