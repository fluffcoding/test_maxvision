from django.contrib import admin


from .models import Order, OrderedProducts, Customer, PrintRecord


class OrderedProductsInline(admin.TabularInline):
    model = OrderedProducts


class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderedProductsInline,
    ]


admin.site.register(Order, OrderAdmin)

admin.site.register(Customer)

admin.site.register(OrderedProducts)

admin.site.register(PrintRecord)