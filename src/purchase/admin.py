from django.contrib import admin

from .models import Supplier, Batch, BatchGroup, BatchChecklist



admin.site.register(Supplier)
admin.site.register(Batch)
admin.site.register(BatchGroup)
admin.site.register(BatchChecklist)