from django.contrib import admin
from . models import Product, Cart, Order, Categorie

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'price', 'category', 'size_options', 'discount', 'discount_price']
    list_filter = ['category', 'discount', ]

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin): 
    prepopulated_fields = {'slug': ('category_name',)}

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'size', 'quantity']
    list_filter = ['user', 'product', 'size', 'quantity']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'date', 'delivered', 'is_paid', 'price']
    list_filter = ['user', 'is_paid', 'delivered']
