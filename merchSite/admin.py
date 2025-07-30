from django.contrib import admin
from . models import Product, Cart, Order, Categorie

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}

admin.site.register(Cart)
admin.site.register(Order)
