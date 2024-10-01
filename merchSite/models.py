from django.db import models
from users.models import User
import datetime
import PIL
from django.views import View
# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100, blank = False, null = False)
    price = models.IntegerField(blank = False, null = False)
    discount = models.BooleanField(default= False)
    discount_price = models.IntegerField(blank = True, null = True)
    description = models.CharField(max_length=255, blank = True, null = True)
    quantity = models.IntegerField(default=1)
    #TEST IMAGE WITH URL
    # Later might use real image stored in database
    image = models.ImageField(upload_to='products', blank = True, null = True)
    slug = models.SlugField(null= True, blank=False)
    

    def __str__(self):
        return self.name
    

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(default = 1)
    price = models.IntegerField(max_length=50, default = '', blank = True, null = True)
    address = models.CharField(max_length=50, blank = True, null = True)
    phone = models.CharField(max_length=50, blank = True, null = True)
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)


    def placeOrder(self):
        self.save()

    @staticmethod
    def get_orders_by_user(user_id):
        return Order.objects.filter(user = user_id).order_by('-date')
    

class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, null = True, blank = True)
    

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE )
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE )

    def get_price(self):
        price = [self.product.price]
        return sum(price)

    
    


