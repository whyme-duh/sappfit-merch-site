from django.shortcuts import render, redirect
from django.http import HttpRequest
from . models import Product, Cart, Order
from django.contrib import messages
from django.http import HttpResponseRedirect
import random
import datetime
# Create your views here.

def index(request):
    featured_products = Product.objects.filter(discount = True)
    return render(request, 'merchSite/home.html', {"products" : featured_products})

def products_page(request):
    products = Product.objects.all()
    return render(request, 'merchSite/productsPage.html', {"products" : products})

def detail_page(request, slug):
    product = Product.objects.get(slug = slug)
    sizes = product.size_options
    category = product.category
    other_products = Product.objects.exclude(category = category)
    similar_products = Product.objects.filter(category = product.category).exclude(slug=slug)
    return render(request, 'merchSite/product-detail.html', {"product": product, "related_products" : similar_products, 'other_products':other_products, "sizes" : sizes})

def add_to_cart(request, id):
    product = Product.objects.get(id = id)
    selected_size = request.POST.get('size')
    quantity = request.POST.get('quantity')
    if selected_size in product.size_options and product.size_options[selected_size] > 0:
        if request.user.is_authenticated:
            Cart.objects.create(user = request.user, product = product, size = selected_size, quantity = quantity)
            messages.success(request, f'Added to Cart')
        else:
            messages.error(request, f'You have to login in order to add items to cart')
    else:
        messages.error(request, f'{selected_size} is out of stock')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def my_cart(request):
    cartitem = Cart.objects.filter(user = request.user)
    total_price = 0
    delivery_cost = 50
    item_costs = 0
    for cart in cartitem:
        if cart.product.discount:
            total_price += cart.product.discount_price * cart.quantity
            item_costs = total_price
        else:
            total_price +=cart.product.price * cart.quantity
            item_costs = total_price

    total_price += delivery_cost     
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        location = request.POST['location']
        phone = request.POST['phone']
        order = Order.objects.create(
            name = name,
            email = email, 
            location = location,
            phone = phone,
            user = request.user,
            price = total_price,
            date = datetime.datetime.now()
        )
        for cart in cartitem:
            if cart.product.discount:
                price = cart.product.discount_price * cart.quantity
            else:
                price = cart.product.price * cart.quantity
            order.add_product(cart.product, cart.size, cart.quantity, price)

        cart.product.size_options[cart.size] -= cart.quantity
        cart.product.save()
        Cart.objects.filter(user = request.user).delete()
        return redirect('checkout')
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



def checkout(request):
    cart = Cart.objects.filter(user = request.user)
    return render(request, 'merchSite/checkout.html')
