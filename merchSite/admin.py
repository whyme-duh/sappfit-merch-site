import json
from django.contrib import admin
from unfold.admin import ModelAdmin
from . models import Product, Cart, Order, Categorie, ReturnProduct
from django.utils.html import format_html

@admin.register(Product)
class ProductAdmin(ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'price', 'category', 'size_options', 'discount', 'discount_price']
    list_filter = ['category', 'discount', ]


@admin.register(Categorie)
class CategorieAdmin(ModelAdmin): 
    prepopulated_fields = {'slug': ('category_name',)}

@admin.register(Cart)
class CartAdmin(ModelAdmin):
    list_display = ['user', 'product', 'size', 'quantity']
    list_filter = ['user', 'product', 'size', 'quantity']

@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ['product', 'user', 'date', 'status', 'is_paid', 'price']
    list_filter = ['user', 'is_paid', 'status']

    
    def status_badge(self, obj):
        colors = {
            'Pending': 'orange',
            'Processing': 'blue',
            'Shipped': 'purple',
            'Delivered': 'green',
            'Cancelled': 'red',
        }
        color = colors.get(obj.status, 'grey')
        return format_html(
            '<span style="color: white; background-color: {}; padding: 3px 10px; border-radius: 10px; font-weight: bold;">{}</span>',
            color,
            obj.status
        )
    status_badge.short_description = 'Status'

@admin.register(ReturnProduct)
class ReturnProductAdmin(ModelAdmin):
    list_display = ['user', 'product', 'size', 'quantity', 'return_status', 'return_request_date']
    list_filter = ['user', 'product', 'size', 'quantity', 'return_status', 'return_request_date']

