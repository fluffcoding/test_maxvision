from django.contrib import admin

from .models import WarehouseLocation, Product, Category, Material, Size, Color, Model, Characteristics




admin.site.register(Category)
admin.site.register(Material)
admin.site.register(Size)
admin.site.register(Color)
admin.site.register(Model)
admin.site.register(Characteristics)
admin.site.register(WarehouseLocation)
admin.site.register(Product)