from django.urls import path

from .views import returns, returnsList

app_name = 'administer'

urlpatterns = [
    path('returns', returns, name='returns'),
    # api
    path('returns-list', returnsList, name='returnsList'),
]