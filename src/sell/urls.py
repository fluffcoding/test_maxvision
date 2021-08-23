from django.urls import path
from .views import advertsDelete, advertsUpdate, main, advertsList


app_name = 'sell'

urlpatterns = [
    path('', main, name='main'),

    # api
    path('list', advertsList, name='list'),
    path('update', advertsUpdate, name='update'),
    path('delete', advertsDelete, name='delete'),
]
