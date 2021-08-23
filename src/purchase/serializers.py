from django.db.models.lookups import StartsWith
from rest_framework import response, serializers

from .models import Batch, BatchGroup, Supplier


# from product.serializers import ProductSerializer

import pandas as pd

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'


class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = ('id','product','quantity','price','remaining', 'shipping_info', 'stock_status', 'batch_group_status')
        # fields = '__all__'
    
    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['product'] = ProductSerializer(instance.product).data
    #     df = pd.json_normalize(response, sep='_')
    #     e = (df.to_dict(orient='records')[0])
    #     return e

class BatchGroupSerializer(serializers.ModelSerializer):
    bg_id = serializers.CharField(source='id')
    supplier = serializers.CharField(source='supplier.name')

    class Meta:
        model = BatchGroup
        fields = ('bg_id', 'id', 'total_price','batches', 'supplier', 'order_date', 'status', 'payment_status', 'transport_status', 'import_status', 'expected_delivery_date', 'receipt_date',)


    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['bg_id'] = f'B{response["id"]}'
        return response