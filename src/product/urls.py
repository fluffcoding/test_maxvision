from django.urls import path
from .views import main, new, apiList, apiUpdate, apiIncompleteList, apiCharacteristicsList, apiAddCharacteristic
# , tutorial


app_name = 'product'

urlpatterns = [
    path('', main, name='main'),
    path('new', new, name='new'),
    # api
    path('list', apiList, name='list'),
    path('update', apiUpdate, name='update'),
    # incomplete products
    path('incomplete-list', apiIncompleteList, name='incomplete-list'),
    # characteristics
    path('all-characteristics', apiCharacteristicsList, name='all-characteristics'),
    path('add-characteristic', apiAddCharacteristic, name='add-characteristic')
]
