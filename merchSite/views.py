from django.shortcuts import render
from django.http import HttpRequest
from . models import Product, Cart, CartItem
from django.contrib import messages
from django.http import HttpResponseRedirect

# Create your views here.

def index(request):
    products = Product.objects.all()
    return render(request, 'merchSite/home.html', {"products" : products})

def detail_page(request, slug):
    product = Product.objects.get(slug = slug)
    return render(request, 'merchSite/product-detail.html', {"product": product})

def add_to_cart(request, id):
    product = Product.objects.get(id = id)
    user = request.user
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user = user, product= product)
        messages.success(request, f'Added to Cart')
    else:
        messages.error(request, f'You have to login in order to add items to cart')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def my_cart(request):
    cartitem = Cart.objects.get(user = request.user)
    return render(request, 'merchSite/cart.html', {"cartitem": cartitem})
