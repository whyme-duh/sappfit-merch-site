from django.shortcuts import render
from django.http import HttpRequest
from . models import Product, Cart, CartItem
from django.contrib import messages
from django.http import HttpResponseRedirect
import random

# Create your views here.

def index(request):
    products = Product.objects.all()
    return render(request, 'merchSite/home.html', {"products" : products})

def detail_page(request, slug):
    product = Product.objects.get(slug = slug)
    product_ids = []
    product_array = []
    products = Product.objects.all()
    for p in products:
        product_ids.append(p.id)
    
    for i in range(3):
        rn = random.choice(product_ids)
        product_array.append(Product.objects.filter(id=rn).exclude(slug=slug))
    return render(request, 'merchSite/product-detail.html', {"product": product, "other_products" : product_array})

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
    item_costs = 0
    for cart in cartitem:
        if cart.product.discount:
            total_price += cart.product.discount_price
            item_costs = total_price
        else:
            total_price +=cart.product.price
            item_costs = total_price

    total_price += delivery_cost        

    return render(request, 'merchSite/cart.html', {"cartitem": cartitem, "total_price": total_price, "delivery_cost": delivery_cost, "item_costs": item_costs})


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

