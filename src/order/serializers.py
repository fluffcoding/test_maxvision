from rest_framework import serializers
# from rest_framework import response
# from rest_framework.response import Response

# from product.serializers import ProductSerializer, OrderedProductsSerializer

from sell.serializers import PlatformSerializer

from .models import Customer, Order, OrderedProducts

import pandas as pd

from product.serializers import ProductSerializer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['name', 'street_name','house_number','zip_code','city',]
    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['name'] = instance.full_name()
    #     return response


        
class OrderSerializer(serializers.ModelSerializer):
    
    # products = OrderedProductsSerializer(many=True)
    # category = serializers.CharField(source='products.product.characteristics.category.name')
    class Meta:
        model = Order
        fields = '__all__'
        # exclude = None


    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['customer'] = CustomerSerializer(instance.customer).data
        response['platform'] = PlatformSerializer(instance.platform).data["name"]
        return response



class OrderedProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderedProducts
        fields = ( 'id','quantity', 'due_date')


    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['order'] = OrderSerializer(instance.order).data
        response['product'] = ProductSerializer(instance.product).data
        df = pd.json_normalize(response, sep='_')
        e = (df.to_dict(orient='records')[0])
        return e

    
