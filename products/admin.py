from django.contrib import admin

# Register your models here.
from . import models


@admin.register(models.ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name", "id",
    )
    search_fields = ("name",)


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "product_type",
        "price",
        "quantity",
        "pk",
    )
    search_fields = ("name", "product_id",)
    list_filter = ("product_type", "category",)
