from django.shortcuts import render

from rest_framework.decorators import api_view

from rest_framework.response import Response

from .models import Advertisement

from .serializers import AdvertisementSerializer

# Create your views here.

nav = {
    'dashboard': 'white',
    'orders': 'white',
    'selling': 'warning',
    'products': 'white',
    'purchasing': 'white',
    'inventory': 'white',
    'administer': 'white',
    'analysis': 'white',
}


def main(request):
    title = 'Selling'
    context = {
        'title': title,
        'nav': nav,
    }
    return render(request, 'sell/main2.html', context)



@api_view(['GET'])
def advertsList(request):
    adverts = Advertisement.objects.all()
    serializer = AdvertisementSerializer(adverts, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def advertsUpdate(request):
    advert = Advertisement.objects.get(id=request.data.get('id'))
    advert.delivery_date = request.data.get('delivery_date')
    advert.save()
    return Response(f'{advert.title} modified.')


@api_view(['POST'])
def advertsDelete(request):
    advert = Advertisement.objects.get(id=request.data.get('id'))
    # advert.delivery_date = request.data.get('delivery_date')
    advert.delete()
    print('deleted')
    return Response(f'{advert.title} deleted.')