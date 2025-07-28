from django.contrib import admin
from . models import Product, Cart, Order

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Cart)
admin.site.register(Order)
