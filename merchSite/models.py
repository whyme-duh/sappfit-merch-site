from django.db import models
from users.models import User
import datetime
import PIL
from django.views import View
from django.forms import fields, forms
from ckeditor.fields import RichTextField
from django.db.models import JSONField
# Create your models here.


# class Size(models.Model):
#     option = models.CharField(max_length=10, blank = True, null = True)

#     def __str__(self):
#         return self.option


class Product(models.Model):
    name = models.CharField(max_length=100, blank = False, null = False)
    price = models.IntegerField(blank = False, null = False)
    discount = models.BooleanField(default= False)
    discount_price = models.IntegerField(blank = True, null = True)
    description = RichTextField(blank= True, null = True)
    #TEST IMAGE WITH URL
    # Later might use real image stored in database
    image = models.ImageField(upload_to='products', blank = True, null = True)
    second_image = models.ImageField(upload_to='products', blank = True, null = True)
    third_image = models.ImageField(upload_to='products', blank = True, null = True)
    fourth_image = models.ImageField(upload_to='products', blank = True, null = True)
    slug = models.SlugField(null= True, blank=False)
    category = models.CharField(max_length=50, blank=True, null=True)
    size_options = JSONField(default=dict)

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
    status = models.BooleanField(default=False)
    name = models.CharField(max_length = 80, blank = True, null = True)
    location = models.CharField(max_length = 80, blank = True, null = True)
    email = models.EmailField(max_length = 80, blank = True, null = True)
    phone = models.IntegerField( blank = True, null = True)
    size = models.CharField(max_length = 80, blank = True, null = True)
    quantity = models.IntegerField( blank = True, null = True)

    def __str__(self):
        return f"Order from {self.name} ({self.user}) - {self.product} - size ({self.size}) - quantity ({self.quantity})"

    def placeOrder(self):
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

    


    
    


