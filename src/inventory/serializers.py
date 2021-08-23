from purchase.models import ShippingInfo


from rest_framework import response, serializers



class ShippingInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingInfo
        fields = '__all__'
