from django.db import models

from order.models import OrderedProducts

choices = {
    'returns_status': [
        ('Accepted','Accepted'),
        ('Rejected','Rejected'),
        ('Pending','Pending'),
    ]
}


class Return(models.Model):
    ordered_product = models.ForeignKey(OrderedProducts, on_delete=models.SET_NULL, null=True, blank=True)
    return_request = models.TextField()
    status = models.CharField(choices=choices['returns_status'], max_length=20)