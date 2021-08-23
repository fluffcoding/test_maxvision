from django.urls import path

from .views import main, batchGroupsList, productBatchesList, suppliersList, supplierCreate, batchesList, batchUpdate, batchGroupEdit, confirmBatchGroup, batchGroupSingle, batchGroupConfirm

app_name = 'purchase'

urlpatterns = [
   path('', main, name='main'),
   path('confirm-bg/<id>/', confirmBatchGroup, name='confirm-bg'),
   # api
   path('batch-group-single/<id>/', batchGroupSingle, name='bg-single'),
   path('batch-group-list', batchGroupsList, name='bg-list'),
   path('product-batch-list', productBatchesList, name='product-batch-list'),
   path('batch-list', batchesList, name='batch-list'),
   path('batch-update', batchUpdate, name='batch-update'),
   path('batch-group-edit', batchGroupEdit, name='bg-edit'),
   path('batch-group-confirm', batchGroupConfirm, name='bg-confirm'),
   path('suppliers-list', suppliersList, name='suppliers-list'),
   path('supplier-create', supplierCreate, name='supplier-create'),
]
