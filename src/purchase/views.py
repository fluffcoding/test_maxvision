from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from rest_framework import serializers

from product.serializers import BatchProductSerializer

from rest_framework.decorators import api_view

from rest_framework.response import Response


from .serializers import BatchSerializer, BatchGroupSerializer, SupplierSerializer

from .models import Batch, BatchGroup, Supplier

from product.models import Product


nav = {
    'dashboard': 'white',
    'orders': 'white',
    'selling': 'white',
    'products': 'white',
    'purchasing': 'warning',
    'inventory': 'white',
    'administer': 'white',
    'analysis': 'white',
}



def main(request):
    context = {
        'nav': nav,
        'title': 'Purchasing'
    }
    return render(request, 'purchase/main.html', context)




def confirmBatchGroup(request, id):
    batchGroup = BatchGroup.objects.get(id=id)
    if batchGroup.status == 'Concept':
        context = {
            'nav': nav,
            'title': 'Confirm Batch Group',
            'batch_group': batchGroup,
            'id': id,
        }
        return render(request, 'purchase/confirm.html', context)
    else:
        return redirect('purchase:main')

@api_view(['GET'])
def batchGroupSingle(request, id):
    batchGroup = BatchGroup.objects.get(id=id)
    serializer = BatchGroupSerializer(batchGroup, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def batchGroupsList(request):
    batchGroups = BatchGroup.objects.all()
    serializer = BatchGroupSerializer(batchGroups, many=True)
    return Response(serializer.data)



@api_view(['GET'])
def productBatchesList(request):
    products = Product.objects.exclude(characteristics=None)
    serializer = BatchProductSerializer(products, many=True)
    # batches = Batch.objects.filter(product__in=products)
    # serializer = BatchSerializer(batches, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def suppliersList(request):
    suppliers = Supplier.objects.all()
    serializer = SupplierSerializer(suppliers, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def supplierCreate(request):
    supplier = Supplier.objects.get(name=request.data.get('name'))
    date = request.data.get('date')
    batchGroup = BatchGroup.objects.create(supplier=supplier, order_date=date, status='Concept')
    batchGroup.save()
    return Response(f' Batch Group Created')
    

@api_view(['GET'])
def batchesList(request):
    batches = Batch.objects.all()
    serializer = BatchSerializer(batches, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def batchUpdate(request):
    print(request.data)
    batch = Batch.objects.get(id=request.data.get('id'))
    # batch.product = request.data.get('product')
    batch.quantity = request.data.get('quantity')
    batch.price = request.data.get('price')
    batch.save()

    return Response(f'Batch #{batch.id} has been updated.')


@api_view(["POST"])
def batchGroupEdit(request):
    bg = BatchGroup.objects.get(id=request.data.get('bg_id'))
    batch_ids = request.data.get('batch_id')
    batches = Batch.objects.filter(id__in=batch_ids)
    for batch in batches:
        if request.data.get('remove')==True:
            batch.group = None
            batch.save()
            return Response(f'{batch_ids} removed from {bg.id}')
        else:
            batch.id = None
            batch.group = bg
            batch.save()
            return Response(f'{batch_ids} added to {bg.id}')
        # print(request.data)


@api_view(['POST'])
def batchGroupConfirm(request):
    # print(request.data)
    bg = BatchGroup.objects.get(id=request.data.get('bg')['id'])
    bg.batches.clear()
    for item in request.data.get('csv'):
        batch = Batch.objects.get(id=int(item['id']))
        # print(batch.total_price())
        batch.product = Product.objects.get(id=int(item['product']))
        batch.quantity = int(item['quantity'])
        batch.price = float(item['price'])
        # print(batch.total_price())
        batch.save()
        bg.batches.add(batch)
    bg.status = 'Ordered'
    bg.save()
    # bg = BatchGroup.objects.get(id=request.data.get('id'))
    return Response('yay')