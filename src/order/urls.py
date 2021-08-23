from django.urls import path

from .views import ordersList, main, printRecords, ordersUpdate, ordersPrint, printView, testMain

app_name = 'order'

urlpatterns = [
    path('', main, name='main'),
    path('test', testMain, name='test'),
    path('print', printRecords, name='print-records'),
    # api
    path('list/', ordersList, name='list'),
    path('update/', ordersUpdate, name='update'),
    path('print/', ordersPrint, name='print'),
    path('print/<id>/', printView, name='print-view'),

]