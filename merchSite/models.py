from django.db import models

from django.contrib.auth.models import User
import datetime
import PIL
from django.views import View
from django.forms import fields, forms
from ckeditor.fields import RichTextField
from django.db.models import JSONField
import json
# Create your models here.


# class Size(models.Model):
#     option = models.CharField(max_length=10, blank = True, null = True)

#     def __str__(self):
#         return self.option

class Categorie(models.Model):
    category_name = models.CharField(max_length=100, null = True, blank = True)
    slug = models.SlugField(null= True, blank=False)

    def __str__(self):
        return self.category_name


class Product(models.Model):
    name = models.CharField(max_length=100, blank = False, null = False)
    price = models.IntegerField(blank = False, null = False)
    discount = models.BooleanField(default= False)
    discount_price = models.IntegerField(blank = True, null = True)
    description = RichTextField(blank= True, null = True)
    image = models.ImageField(upload_to='products', blank = True, null = True)
    second_image = models.ImageField(upload_to='products', blank = True, null = True)
    third_image = models.ImageField(upload_to='products', blank = True, null = True)
    fourth_image = models.ImageField(upload_to='products', blank = True, null = True)
    slug = models.SlugField(null= True, blank=False)
    category = models.ForeignKey(Categorie, on_delete = models.CASCADE, null = True, blank = True)
    size_options = JSONField(default= dict)
    product_available_text = models.TextField(max_length=100, blank = True, null = True)

    def __str__(self):
        return self.name
    
        
    
# class ProductVarient(models.Model):
#     product = models.ForeignKey(Product, on_delete = models.CASCADE, blank = True, null = True, related_name = 'product_varient')
#     size = models.ForeignKey(Size, on_delete = models.CASCADE, blank = True, null = True)
#     quantity = models.PositiveIntegerField(default = 0, blank = True, null = True)

#     class Meta:
#         unique_together = ('product', 'size')

#     def __str__(self):
#         return f"{self.product.name} - {self.size.option} (quantity = {self.quantity})"

class Order(models.Model):
    product = models.TextField(blank = True, null = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.IntegerField( default = '', blank = True, null = True)
    date = models.DateTimeField(auto_now_add=True)
    delivered = models.BooleanField(default=False)
    name = models.CharField(max_length = 80, blank = True, null = True)
    location = models.CharField(max_length = 80, blank = True, null = True)
    email = models.EmailField(max_length = 80, blank = True, null = True)
    phone = models.IntegerField( blank = True, null = True)
    is_paid = models.BooleanField(default=False, null = True, blank = True)
    order_id = models.TextField(blank = True, null = True)
    transaction_id = models.TextField(blank = True, null = True)

    def __str__(self):
        return f"Order from {self.name} ({self.user}) - {self.product} "

    def add_product(self, product, size, quantity, price):
        product_data = {
            'id': product.id,
            'product': product.name, 
            'size': size,
            'quantity': quantity,
            'price': price,
            'reviewed': False
        }
        if self.product:
            product_list = json.loads(self.product)
        else:
            product_list = []
        product_list.append(product_data)
        self.product = json.dumps(product_list)
        self.save()

    @staticmethod
    def get_orders_by_user(user_id):
        return Order.objects.filter(user = user_id).order_by('-date')
    

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank = True, null = True)
    size = models.TextField(max_length=50, blank = True, null = True)
    quantity = models.IntegerField(blank= True, null = True)

    def __str__(self):
        return f"Cart for {self.user}"

    


    
    


