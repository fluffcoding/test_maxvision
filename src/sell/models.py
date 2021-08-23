from django.db import models

from product.models import Product
# from order.models import Order


class Platform(models.Model):
    name = models.CharField(max_length=50)


    def __str__(self):
        return self.name


class Advertisement(models.Model):
    platforms = models.ManyToManyField(Platform)
    title = models.CharField(max_length=100, null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    ean = models.CharField(max_length=50)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    delivery_date = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='advertisement/', null=True, blank=True)


# class Returns(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)