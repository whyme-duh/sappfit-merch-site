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
    dict = {
        "L" : 1,
        "S" : 1,
        "M" : 1
    }
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
    
    def discount_rate(self):
        if self.discount:
            return f'-{int(((self.price-self.discount_price)/self.price) * 100)}%'
    
    
   
class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending' , 'Pending'),
        ('Processing' , 'Processing'),
        ('Shipped' , 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled' , 'Cancelled')
    )
    CANELLATION_REASONS = (
        ('I selected wrong product.' , 'I selected wrong product.'),
        ('I forgot to add other products.' , 'I forgot to add other products.'),
        ("I don't plan to buy this product right now! " , "I don't plan to buy this product right now!"),
        ('Other' , 'Other')
    )
    product = models.TextField(blank = True, null = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank = True)
    price = models.IntegerField(default = '', blank = True, null = True)
    date = models.DateTimeField(auto_now_add=True)
    delivered_date = models.DateTimeField('delivered_date', null = True, blank = True)
    status = models.CharField(max_length=20, choices= STATUS_CHOICES, default='Pending')
    name = models.CharField(max_length = 80, blank = True, null = True)
    location = models.CharField(max_length = 80, blank = True, null = True)
    email = models.EmailField(max_length = 80, blank = True, null = True)
    phone = models.CharField(max_length = 100, blank = True, null = True)
    is_paid = models.BooleanField(default=False, null = True, blank = True)
    order_id = models.CharField(max_length = 1000, blank = True, null = True)
    transaction_id = models.CharField(max_length = 1000, blank = True, null = True)
    cancellation_reasons = models.CharField(max_length=100, blank = True, null= True)
    cancellation_other_reason = models.TextField(max_length=50, blank = True, null = True)


    def __str__(self):
        return f"{self.id} Order from {self.name} ({self.user}) - {self.product} "

    def add_product(self, product, size, quantity, price):
        product_data = {
            'order_id' : self.id,
            'id': product.id,
            'product': product.name, 
            'size': size,
            'quantity': quantity,
            'price': price,
            'reviewed': False,
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
    
    def save(self, *args, **kwargs):
        if self.status == "Delivered":
            self.delivered_date = datetime.datetime.now()
        else:
            self.delivered_date = None
        super(Order, self).save(*args, **kwargs)

   
    

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank = True)
    session_id = models.CharField(max_length=40, null= True, blank = True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank = True, null = True)
    size = models.TextField(max_length=50, blank = True, null = True)
    quantity = models.IntegerField(blank= True, null = True)

    @property
    def get_total_cost(self):
        if self.product.discount:
            return self.product.discount_price * self.quantity
        return self.product.price * self.quantity

    def __str__(self):
        return f"Cart for {self.user}"
    

    def get_discounted_price(self):
        return self.product.price - self.product.discount_price
    


class ReturnProduct(models.Model):
    RETURN_STATUS = (
        ("None" , "None"),
        ("Pending" , "Pending"),
        ("Returning" , "Returning"),
        ("Returned" , "Returned"),

    )
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete = models.PROTECT)
    size = models.CharField(max_length=10, null = True, blank = True)
    quantity = models.CharField(max_length=10, null = True, blank = True)
    order = models.ForeignKey(Order, on_delete= models.PROTECT, null= True, blank = True)
    return_status = models.CharField(max_length=100, choices=RETURN_STATUS, default="Pending")
    return_request_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} requested return on {self.product}'




    


    


    
    


