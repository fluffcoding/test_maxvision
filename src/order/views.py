from django.shortcuts import render

from django.urls import reverse_lazy

from .models import Order, OrderedProducts, PrintRecord, Customer
from .serializers import OrderedProductsSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

import pandas as pd

from product.models import Product

import json

pages = [
    {
    'id': 1,
    'name': 'Outstanding Orders',
    'url': reverse_lazy('order:main'),
    'is_active': False,
    },
    {
    'id': 2,
    'name': 'Print Records',
    'url': reverse_lazy('order:print-records'),
    'is_active': False,
    },
    ]

nav = {
    'dashboard': 'white',
    'orders': 'warning',
    'selling': 'white',
    'products': 'white',
    'purchasing': 'white',
    'inventory': 'white',
    'administer': 'white',
    'analysis': 'white',
}



def main(request):
    title = 'Outstanding Orders'
    pages[1]['is_active'] = False
    pages[0]['is_active'] = True
    context = {
        'title': title,
        'pages': pages,
        'nav': nav,
    }
    return render(request, 'order/main.html', context)



def testMain(request):
    title = 'Outstanding Orders'
    pages[1]['is_active'] = False
    pages[0]['is_active'] = True
    context = {
        'title': title,
        'pages': pages,
        'nav': nav,
    }
    return render(request, 'order/test_main.html', context)




def printRecords(request):
    pages[1]['is_active'] = True
    pages[0]['is_active'] = False
    title='Print Records'
    print_records = PrintRecord.objects.all().order_by('-created')
    context = {
        'title': title,
        'pages': pages,
        'records': print_records,
        'nav': nav,
    }
    return render(request, 'order/print_records.html', context)


def printView(request, id):
    record = PrintRecord.objects.get(id=id)
    ordered_products = record.ordered_products.all()
    data = OrderedProductsSerializer(ordered_products, many=True).data
    data = json.dumps(data)
    def returnID(order):
        return order.id
    ids = map(returnID, ordered_products)
    ids = list(ids)
    context = {
        'record': record,
        'nav': nav,
        'data': data,
    }
    return render(request, 'print/postnl.html', context)


@api_view(['GET'])
def ordersList(request):
    orders = OrderedProducts.objects.all()
    serializer = OrderedProductsSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def ordersUpdate(request):
    ids = request.data.get('ids')
    changeTo = request.data.get('change')
    items = Order.objects.filter(id__in=ids)
    items.update(status=changeTo.capitalize())
    return Response(f'{len(ids)} orders modified.')


@api_view(['POST'])
def ordersPrint(request):
    print(request.data)
    order_ids = request.data.get('orders')
    ordered_products_ids = request.data.get('ordered_products')
    ordered_products = OrderedProducts.objects.filter(id__in=ordered_products_ids)
    orders = Order.objects.filter(id__in=order_ids)
    # orders = Order.objects.filter()        
    orders.update(status="Printed")
    printRecord = PrintRecord.objects.create()
    printRecord.ordered_products.set(ordered_products_ids)
    print(printRecord.ordered_products)
    printRecord.save()
    return Response(printRecord.id)