from django.shortcuts import render
from django.http import HttpRequest
from . models import Product


# Create your views here.

def index(request):
    products = Product.objects.all()
    return render(request, 'merchSite/home.html', {"products" : products})


def sign_up(request):
    return render(request, 'merchSite/signup.html')