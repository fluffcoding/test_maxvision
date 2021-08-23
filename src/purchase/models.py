from django.db import models

from django.db.models.signals import post_save

from product.models import Product

choices = {
    'BG_status': [
        ('Ordered','Ordered'),
        ('Concept','Concept'),
        ('Received','Received'),
    ]
}



class ShippingInfo(models.Model):
    weight= models.IntegerField(null=True, blank=True)
    length= models.IntegerField(null=True, blank=True)
    width= models.IntegerField(null=True, blank=True)
    height= models.IntegerField(null=True, blank=True)




class Supplier(models.Model):
    name = models.CharField(max_length=100)





class BatchGroup(models.Model):
    # batches = models.ManyToManyField(Batch, blank=True, related_name='group')
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    order_date = models.DateField(null=True, blank=True)
    status = models.CharField(choices=choices['BG_status'], max_length=20, null=True, blank=True)
    payment_status = models.BooleanField(default=False)
    transport_status = models.BooleanField(default=False)
    import_status = models.BooleanField(default=False)
    expected_delivery_date = models.DateField(null=True, blank=True)
    receipt_date = models.DateField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)


    def total_price(self):
        price = 0
        for batch in self.batch_set.all():
            if batch.total_price()!=None:
                price += batch.total_price()
        print(price)
        return price


    def batches(self):
        ids = []
        for batch in self.batch_set.all():
            ids.append(batch.id)
        return ids


class Batch(models.Model):
    group = models.ForeignKey(BatchGroup, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    shipping_info = models.ForeignKey(ShippingInfo, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    remaining = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=30, null=True, blank=True)

    def total_price(self):
        if self.price and self.quantity:
            return self.quantity * self.price
        else:
            return None

    def stock_status(self):
        if self.remaining != None:
            if self.remaining<=0:
                return 'Out of Stock'
            else:
                return 'In Stock'
        else:
            return 'Incomplete Batch'


    def batch_group_status(self):
        return 'Under Construction'
        # data = list(self.group.all().order_by('-created').values('id','status','created'))
        # bg = None
        
        # if len(data) > 0:
        #     bg = data[0]
        #     if self.status==None:
        #         self.status = bg['status']
        #         self.save()

        # return self.status



def create_batch(sender, instance, created, **kwargs):
    
    if created:
        print(instance.id)
        # print(sender)
        batch = Batch.objects.create(product=instance)
        # batch.product = Product.objects.get(id=instance.id)
        batch.shipping_info = ShippingInfo.objects.create()
        batch.save()
        print('Batch created')

# Signal to create empty batch everytime a product is created
post_save.connect(create_batch, sender=Product)






class BatchChecklist(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True, blank=True)
    quantity_received = models.IntegerField(null=True, blank=True)
