from django.db import models
from django.contrib.auth.models import User

from merchSite.models import Product


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)


    def __str__(self):
        return self.user.username
    

class Review(models.Model):
    review = models.CharField(max_length=100, blank = True, null = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank = True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, null = True, blank = True)
    review_star = models.IntegerField(max_length=1, null = True, blank = False)

    def __str__(self):
        return f'Review by {self.user.username} on {self.product}: rated {self.review_star}'