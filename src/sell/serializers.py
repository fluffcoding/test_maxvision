from rest_framework import serializers

from .models import Advertisement, Platform

import pandas as pd

from product.serializers import ProductSerializer


class AdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = '__all__'


    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['product'] = ProductSerializer(instance.product).data
        df = pd.json_normalize(response, sep='_')
        e = (df.to_dict(orient='records')[0])
        return e




class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = ('name',)