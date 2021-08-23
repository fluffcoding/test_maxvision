from order.models import Order


from rest_framework import response, serializers

from .models import Return

from order.serializers import OrderedProductsSerializer

import pandas as pd

class ReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Return
        fields = '__all__'


    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['ordered_product'] = OrderedProductsSerializer(instance.ordered_product).data
        df = pd.json_normalize(response, sep='_')
        e = (df.to_dict(orient='records')[0])
        return e