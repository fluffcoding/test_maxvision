from rest_framework import serializers
from rest_framework import response
from rest_framework.response import Response


from .models import Characteristics, Product

from purchase.serializers import BatchSerializer

from purchase.models import Batch

# from order.serializers import OrderedProductsSerializer
from order.models import OrderedProducts

import pandas as pd

from .models import Category, Material, Size, Color, Model


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)
class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ('name',)
class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ('name',)
class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ('name',)
class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = ('name',)


class CharacteristicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Characteristics
        fields = ('reference',)


class CompleteCharacteristicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Characteristics
        fields = ('reference', 'id', )

    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        # response['category'] = CategorySerializer(instance.category).data["name"]
        response['material'] = MaterialSerializer(instance.material).data["name"]
        response['size'] = SizeSerializer(instance.size).data["name"]
        response['color'] = ColorSerializer(instance.color).data["name"]
        response['model'] = ModelSerializer(instance.model).data["name"]
        return response


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='characteristics.category.name', default='None')
    class Meta:
        model = Product
        fields = ('id','functionality','title','description','warehouse','category','latest_batch_id')
    # ('id','title', 'category' )
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['characteristics'] = CharacteristicsSerializer(instance.characteristics).data
        df = pd.json_normalize(response, sep='_')
        e = (df.to_dict(orient='records')[0])
        return e

class BatchProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='characteristics.category.name', default='None')
    class Meta:
        model = Product
        fields = ('id','functionality','title','description','warehouse','category','latest_batch_id', )
    # ('id','title', 'category' )
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['characteristics'] = CharacteristicsSerializer(instance.characteristics).data
        # print(instance.latest_batch_id())
        try:
            latest_batch = Batch.objects.get(id=instance.latest_batch_id())
        except:
            latest_batch = None
        # print(instance.characteristics)
        # print(instance.latest_batch_id)
        response['batch'] = BatchSerializer(latest_batch).data
        df = pd.json_normalize(response, sep='_')
        e = (df.to_dict(orient='records')[0])
        return e


class CompleteProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='characteristics.category.name', default='None')
    class Meta:
        model = Product
        fields = ['id', 'date_created', 'category',
         'functionality', 'title', 'description', 'image', 'reference', 'warehouse', 'latest_batch_id', 'warehouse_number']
    # ('id','title', 'category' )
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['characteristics'] = CompleteCharacteristicsSerializer(instance.characteristics).data
        df = pd.json_normalize(response, sep='_')
        e = (df.to_dict(orient='records')[0])
        return e

