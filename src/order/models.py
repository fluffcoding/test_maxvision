from django.db import models
from django.db.models.fields import related

from product.models import Product
from sell.models import Platform, Advertisement

choices = {
    'status': [
    ("Complete", "Complete"),
    ("Confirmed", "Confirmed"),
    ("Deleted", "Deleted"),
],
    'gender': [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    ]
}


class BillingInfo(models.Model):
    first_name = models.CharField(null=True, blank=True, max_length=100)
    surname = models.CharField(null=True, blank=True, max_length=100)
    sex = models.CharField(choices=choices["gender"], max_length=100, null=True, blank=True)
    street_name = models.CharField(null=True, blank=True, max_length=100)
    house_number = models.CharField(null=True, blank=True, max_length=100)
    house_number_extension = models.CharField(null=True, blank=True, max_length=100)
    zip_code = models.CharField(max_length=10, null=True, blank=True)
    city = models.CharField(null=True, blank=True, max_length=100)
    country = models.CharField(null=True, blank=True, max_length=100)
    email = models.EmailField(null=True, blank=True)
    extra_info = models.TextField(null=True, blank=True)
    company= models.CharField(null=True, blank=True, max_length=100)
    extra_address_information = models.TextField(null=True, blank=True)
    vat_number = models.CharField(max_length=25, null=True, blank=True)
    kvk_number = models.CharField(max_length=25, null=True, blank=True)
    order_reference = models.CharField(max_length=50, null=True, blank=True)


class Customer(models.Model):
    first_name = models.CharField(null=True, blank=True, max_length=100)
    surname = models.CharField(null=True, blank=True, max_length=100)
    sex = models.CharField(choices=choices["gender"], max_length=100, null=True, blank=True)
    street_name = models.CharField(null=True, blank=True, max_length=100)
    house_number = models.CharField(null=True, blank=True, max_length=100)
    house_number_extension = models.CharField(null=True, blank=True, max_length=100)
    zip_code = models.CharField(max_length=10, null=True, blank=True)
    city = models.CharField(null=True, blank=True, max_length=100)
    country = models.CharField(null=True, blank=True, max_length=100)
    email = models.EmailField(null=True, blank=True)
    extra_info = models.TextField(null=True, blank=True)
    company= models.CharField(null=True, blank=True, max_length=100)
    extra_address_information = models.TextField(null=True, blank=True)
    delivery_phone_number = models.CharField(max_length=20, null=True, blank=True)
    language = models.CharField(max_length=10, null=True, blank=True)


    def name(self):
        return self.first_name + ' ' + self.surname



class Order(models.Model):
    platform = models.ForeignKey(Platform, on_delete=models.SET_NULL, null=True, blank=True)
    # products = models.ManyToManyField() # Incomplete
    status = models.CharField(choices=choices["status"], max_length=50, default='Confirmed')
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    billing_info = models.ForeignKey(BillingInfo, on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateField(null=True, blank=True)
    # products = models.ManyToManyField('OrderedProducts', related_name='ordered_products', blank=True)


class OrderedProducts(models.Model):
    ad = models.ForeignKey(Advertisement, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    order_item_id = models.CharField(max_length=20, null=True, blank=True)
    cancellation_request = models.BooleanField(default=False)
    due_date = models.DateField(null=True, blank=True)
    latest_delivery_date = models.DateField(null=True, blank=True)
    exact_delivery_date = models.DateField(null=True, blank=True)
    offer_id = models.CharField(null=True, blank=True, max_length=50)
    reference = models.CharField(null=True, blank=True, max_length=50)
    ean = models.CharField(null=True, blank=True, max_length=50)
    title = models.CharField(null=True, blank=True, max_length=200)
    quantity_shipped = models.IntegerField(null=True, blank=True)
    quantity_cancelled = models.IntegerField(null=True, blank=True)
    unit_price = models.FloatField(null=True, blank=True)
    commission = models.FloatField(null=True, blank=True)


class PrintRecord(models.Model):
    # orders = models.ManyToManyField(Order)
    ordered_products = models.ManyToManyField(OrderedProducts)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
