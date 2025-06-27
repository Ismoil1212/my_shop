from django.contrib import admin
from goods.models import Categories, Products


@admin.register(Categories)
class CatigoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ["name", "price", "quantity", "discount"]
    list_filter = ["name", "price", "quantity", "discount"]
    list_editable = ["price", "quantity", "discount"]
    search_fields = ["name"]
    fields = [
        "name",
        "category",
        "slug",
        "description",
        "image",
        ("price", "discount"),
        "quantity",
    ]
