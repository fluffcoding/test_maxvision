from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('order/', include('order.urls'), name='order'),
    # path('dashboard/', include('dashboard.urls'), name='dashboard'),
    path('sell/', include('sell.urls'), name='sell'),
    path('product/', include('product.urls'), name='product'),
    # path('analysis/', include('analysis.urls'), name='analysis'),
    path('administer/', include('administer.urls'), name='administer'),
    path('inventory/', include('inventory.urls'), name='inventory'),
    path('purchase/', include('purchase.urls'), name='purchase'),
    path('accounts/', include('allauth.urls')),
    # path('api/', include('api.urls'), name='api'),
    path('admin/', admin.site.urls),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)