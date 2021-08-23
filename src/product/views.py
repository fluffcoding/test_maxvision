from django.shortcuts import render
from django.urls import reverse_lazy

# Create your views here.
from .serializers import CompleteProductSerializer, CategorySerializer, MaterialSerializer, SizeSerializer, ColorSerializer, ModelSerializer


from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.db.models import Q

from .models import Product, Category, Material, Size, Color, Model, Characteristics

pages = [
    {
    'id': 1,
    'name': 'All Products',
    'url': reverse_lazy('product:main'),
    'is_active': False,
    },
    {
    'id': 2,
    'name': 'New Products',
    'url': reverse_lazy('product:new'),
    'is_active': False,
    },
    ]

nav = {
    'dashboard': 'white',
    'orders': 'white',
    'selling': 'white',
    'products': 'warning',
    'purchasing': 'white',
    'inventory': 'white',
    'administer': 'white',
    'analysis': 'white',
}

def main(request):
    title = 'All Products'
    pages[0]['is_active']= True
    pages[1]['is_active']= False
    context = {
        'title': title,
        'pages': pages,
        'nav': nav,
    }
    return render(request, 'product/main.html', context )

def new(request):
    title = 'New Products'
    pages[0]['is_active']= False
    pages[1]['is_active']= True
    context = {
        'title': title,
        'pages': pages,
        'nav': nav,
    }
    return render(request, 'product/new.html', context )
    
    

@api_view(['GET'])
def apiList(request):
    products = Product.objects.exclude(characteristics=None)
    serializer = CompleteProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def apiUpdate(request):
    product = Product.objects.get(id=request.data.get('id'))
    # serializer = CompleteProductSerializer(instance=product, data=request.data)
    data = request.data
    model = Model.objects.get_or_create(name=data.get('characteristics_model'))
    category = Category.objects.get_or_create(name=data.get('category'))
    material = Material.objects.get_or_create(name=data.get('characteristics_material'))
    size = Size.objects.get_or_create(name=data.get('characteristics_size'))
    color = Color.objects.get_or_create(name=data.get('characteristics_color'))
    characteristics = Characteristics.objects.get_or_create(category= category[0],
model=model[0],
material=material[0],
size=size[0],
color=color[0]
)
    product.characteristics = characteristics[0]
    product.functionality = data.get('functionality')
    product.title = data.get('title')
    product.description = data.get('description')
    product.save()

    
    # if serializer.is_valid():
    #     serializer.save()
    return Response(f'{product.title} Modified')






@api_view(['GET'])
def apiIncompleteList(request):
    products = Product.objects.filter(Q(characteristics=None) | Q(warehouse=None))
    serializer = CompleteProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def apiCharacteristicsList(request):
    categories = Category.objects.all()
    materials = Material.objects.all()
    size = Size.objects.all()
    color = Color.objects.all()
    model = Model.objects.all()
    categoriesSerializer = CategorySerializer(categories, many=True)
    materialsSerializer = MaterialSerializer(materials, many=True)
    sizeSerializer = SizeSerializer(size, many=True)
    colorSerializer = ColorSerializer(color, many=True)
    modelSerializer = ModelSerializer(model, many=True)
    data = {
        'categories': categoriesSerializer.data, 
        'materials': materialsSerializer.data, 
        'size': sizeSerializer.data, 
        'color': colorSerializer.data, 
        'model': modelSerializer.data, 
    }
    return Response(data)




@api_view(['POST'])
def apiAddCharacteristic(request):
    product = Product.objects.get(id=request.data.get('selected')['id'])
    chars = request.data.get('data')
    print(chars)
    size = None
    category = None
    color = None
    model = None
    material = None
    try:
        size = Size.objects.get(name=chars['size'])
    except Size.DoesNotExist:
        size = None
    try:
        category = Category.objects.get(name=chars['category'])
    except Category.DoesNotExist:
        category = None
    try:
        color = Color.objects.get(name=chars['color'])
    except Color.DoesNotExist:
        color = None
    try:
        model = Model.objects.get(name=chars['model'])
    except Model.DoesNotExist:
        model = None
    try:
        material = Material.objects.get(name=chars['material'])
    except Material.DoesNotExist:
        material = None
    characteristics, created = Characteristics.objects.get_or_create(size=size, category=category, material=material, color=color, model=model)
    if created:
        characteristics.save()
    
    product.characteristics = characteristics
    product.save()
    product.assign_warehouse()
    print(product.characteristics)
    # if chars.size:
    #     size = chars.size
    # if chars.category:
    #     category = chars.category
    # if chars.color:
    #     category = chars.color
    # if chars.model:
    #     category = chars.model
    # if chars.material:
    #     category = chars.material
    return Response('yay')