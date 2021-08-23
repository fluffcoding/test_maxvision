from django.contrib import admin

# Register your models here.
from .models import Platform, Advertisement


admin.site.register(Platform)
admin.site.register(Advertisement)