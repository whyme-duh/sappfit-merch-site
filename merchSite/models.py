from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100, blank = False, null = False)
    price = models.IntegerField(blank = False, null = False)
    discount = models.BooleanField(default= False)
    discount_price = models.IntegerField(blank = True, null = True)
    quantity = models.IntegerField(default=1)
    #TEST IMAGE WITH URL
    # Later might use real image stored in database
    image = models.URLField(null=True, blank=False)
    slug = models.SlugField(null= True, blank=False)


    def __str__(self):
        return self.name
    


