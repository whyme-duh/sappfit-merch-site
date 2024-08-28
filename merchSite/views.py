from django.shortcuts import render
from django.http import HttpRequest
from . models import Product


# Create your views here.

def index(request):
    products = Product.objects.all()
    return render(request, 'merchSite/home.html', {"products" : products})

def detail_page(request, slug):
    product = Product.objects.get(slug = slug)
    return render(request, 'merchSite/product-detail.html', {"product": product})

