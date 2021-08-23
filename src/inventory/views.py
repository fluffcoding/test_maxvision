from django.shortcuts import render, redirect
from django.urls import reverse_lazy


from rest_framework.decorators import api_view

from rest_framework.response import Response
from inventory.serializers import ShippingInfoSerializer

from purchase.models import ShippingInfo, Batch

from purchase.serializers import BatchSerializer

from django.db.models import Q

pages = [
    {
    'id': 1,
    'name': 'Products Stock',
    'url': '#',
    'is_active': False,
    },
    {
    'id': 2,
    'name': 'Batches Stock',
    'url': reverse_lazy('inventory:batchStock'),
    'is_active': False,
    },
    {
    'id': 3,
    'name': 'Shipping Info',
    'url': reverse_lazy('inventory:shippingInfo'),
    'is_active': False,
    },
    ]


nav = {
    'dashboard': 'white',
    'orders': 'white',
    'selling': 'white',
    'products': 'white',
    'purchasing': 'white',
    'inventory': 'warning',
    'administer': 'white',
    'analysis': 'white',
}



def main(request):
    return redirect('inventory:shippingInfo')


def batchStock(request):
    pages[0]['is_active'] = False
    pages[1]['is_active'] = True
    pages[2]['is_active'] = False
    context = {
        'nav': nav,
        'title': 'Batches Stock',
        'pages': pages,
    }
    return render(request, 'inventory/batch_stock.html', context)



def shippingInfo(request):
    pages[0]['is_active'] = False
    pages[1]['is_active'] = False
    pages[2]['is_active'] = True
    context = {
        'nav': nav,
        'title': 'Shipping Info',
        'pages': pages,
    }
    return render(request, 'inventory/shipping_info.html', context)



@api_view(['GET'])
def shippingInfoList(request):
    shipping_infos = ShippingInfo.objects.all()
    serializer = ShippingInfoSerializer(shipping_infos, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def purchasedBatchList(request):
    purchased_batches = Batch.objects.exclude(Q(status__isnull=True) | Q(status='Concept'))
    serializer = BatchSerializer(purchased_batches, many=True)
    return Response(serializer.data)




@api_view(['POST'])
def shippingInfoUpdate(request):
    item = ShippingInfo.objects.get(id=request.data.get('id'))
    item.weight = request.data.get('weight')
    item.length = request.data.get('length')
    item.width = request.data.get('width')
    item.height = request.data.get('height')
    item.save()
    # print(request.data)
    # shipping_infos = ShippingInfo.objects.all()
    # serializer = ShippingInfoSerializer(shipping_infos, many=True)
    # return Response(serializer.data)
    return Response(f'Shipping Info # {item.id} Updated!')