from django.urls import path


from .views import batchStock, shippingInfo, main, shippingInfoList, shippingInfoUpdate, purchasedBatchList

app_name = 'inventory'

urlpatterns = [
   path('', main, name='main'),
   path('batch-stock', batchStock, name='batchStock'),
   path('shipping-info', shippingInfo, name='shippingInfo'),
   # api
   path('shipping-infos-list', shippingInfoList, name='shippingInfoList'),
   path('shipping-info-update', shippingInfoUpdate, name='shippingInfoUpdate'),
   path('purchased-batch-list', purchasedBatchList, name='purchasedBatchList')
]
