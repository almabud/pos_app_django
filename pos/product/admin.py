from django.contrib import admin
from product import models
# from product.models import Quantity
from product.models import ProductVariant


class ProductVariantAdmin(admin.StackedInline):
    model = ProductVariant
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'product_description']
    inlines = (ProductVariantAdmin,)


# class SupplierTransactionAdmin(admin.ModelAdmin):
#     field_set = ['supplier', 'product', 'date']


admin.site.register(models.Size)
admin.site.register(models.Color)
admin.site.register(models.Category)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.ProductVariant)
admin.site.register(models.Supplier)
admin.site.register(models.SupplierTransaction)
# admin.site.register(models.Quantity)
# admin.site.register(models.ProductTransaction)
