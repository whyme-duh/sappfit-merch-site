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
        Cart.objects.get_or_create(user = user, product= product)
        messages.success(request, f'Added to Cart')
    else:
        messages.error(request, f'You have to login in order to add items to cart')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def my_cart(request):
    cartitem = Cart.objects.filter(user = request.user)
    total_price = 0
    delivery_cost = 50
    for cart in cartitem:
        if cart.product.discount:
            total_price += cart.product.discount_price
        else:
            total_price +=cart.product.price
    total_price += delivery_cost        

    return render(request, 'merchSite/cart.html', {"cartitem": cartitem, "total_price": total_price, "delivery_cost": delivery_cost})


def delete_cart_item(request, id):
    try:
        cart_item = Cart.objects.get(id = id)
        cart_item.delete()
    except Exception as e:
        print(e)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def clear_cart(request):
    Cart.objects.filter(user = request.user).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 

