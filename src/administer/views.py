from django.shortcuts import render

from rest_framework.decorators import api_view

from rest_framework.response import Response

from administer.serializers import ReturnSerializer

from .models import Return

# Create your views here.

nav = {
    'dashboard': 'white',
    'orders': 'white',
    'selling': 'white',
    'products': 'white',
    'purchasing': 'white',
    'inventory': 'white',
    'administer': 'warning',
    'analysis': 'white',
}


def returns(request):
    title = 'Returns'
    context = {
        'title': title,
        # 'pages': pages,
        'nav': nav,
    }
    return render(request, 'administer/returns.html', context)


@api_view(['GET'])
def returnsList(request):
    returns = Return.objects.all()
    serializer = ReturnSerializer(returns, many=True)
    return Response(serializer.data)
