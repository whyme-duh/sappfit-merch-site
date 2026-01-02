import base64
import hashlib
import hmac
from django.shortcuts import render, redirect
from django.http import HttpRequest
from core import settings
from . models import Product, Cart,  Order, Categorie
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
import random
import datetime
from users.models import Review
import requests
from django.contrib.auth.decorators import login_required


def index(request):
    featured_products = Product.objects.filter(discount = True)
    for product in featured_products:
        available_sizes = [size for size, value in product.size_options.items() if value > 0]
        product.product_available_text = "Available in " + ", ".join(available_sizes) + " sizes" if available_sizes else "No sizes available"
    return render(request, 'merchSite/home.html', {"products" : featured_products })

def products_by_category(request, id):
    display = ""
    categories = Categorie.objects.all()
    products = Product.objects.filter(category = id)
    for product in products:
        available_sizes = [size for size, value in product.size_options.items() if value > 0]
        product.product_available_text = "Available in " + ", ".join(available_sizes) + " sizes" if available_sizes else "No sizes available"
    return render(request, 'merchSite/productsByCategory.html', { "products" : products, "categories" : categories, "id": id})

def product_filter_along_with_category(request, id, filter):
    products = Product.objects.all()
    if filter == "lowtohigh":
        products = Product.objects.filter(category = id).order_by('price')
    if filter == "hightolow":
        products = Product.objects.filter(category = id).order_by('-price')
    categories = Categorie.objects.all()
    for product in products:
        available_sizes = [size for size, value in product.size_options.items() if value > 0]
        product.product_available_text = "Available in " + ", ".join(available_sizes) + " sizes" if available_sizes else "No sizes available"
    return render(request, 'merchSite/productsByCategory.html', { "products" : products, "categories" : categories, "id": id})



def products_page(request):
    categories = Categorie.objects.all()
    products = Product.objects.all()
    for product in products:
        available_sizes = [size for size, value in product.size_options.items() if value > 0]
        product.product_available_text = "Available in " + ", ".join(available_sizes) + " sizes" if available_sizes else "No sizes available"
    return render(request, 'merchSite/productsPage.html', { "products" : products, "categories" : categories})

def product_filter(request, filter):
    products = Product.objects.all()
    if filter == "lowtohigh":
        products = Product.objects.all().order_by('price')
    if filter == "hightolow":
        products = Product.objects.all().order_by('-price')
    categories = Categorie.objects.all()
    for product in products:
        available_sizes = [size for size, value in product.size_options.items() if value > 0]
        product.product_available_text = "Available in " + ", ".join(available_sizes) + " sizes" if available_sizes else "No sizes available"
    return render(request, 'merchSite/productsPage.html', { "products" : products, "categories" : categories, 'active_filter': filter})



def detail_page(request, slug):
    product = Product.objects.get(slug = slug)
    reviews = Review.objects.filter(product = product)
    product_original_price = product.price
    product_price_with_discount = product.discount_price
    # this is to find the discount rate
    if product_price_with_discount:
        discount_rate = int(((product_original_price-product_price_with_discount)/product_original_price)*100)
    else:
        discount_rate = 0

    sizes = product.size_options
    category = product.category
    other_products = Product.objects.exclude(category = category)
    for item in other_products:
        available_sizes = [size for size, value in item.size_options.items() if value > 0]
        item.product_available_text = "Available in " + ", ".join(available_sizes) + " sizes" if available_sizes else "No sizes available"
    similar_products = Product.objects.filter(category = product.category).exclude(slug=slug)
    for item in similar_products:
        available_sizes = [size for size, value in item.size_options.items() if value > 0]
        item.product_available_text = "Available in " + ", ".join(available_sizes) + " sizes" if available_sizes else "No sizes available"
    
    return render(request, 'merchSite/product-detail.html', {"product": product, "related_products" : similar_products, 'other_products':other_products, "sizes" : sizes, "reviews": reviews, "discount_rate" : discount_rate})

def get_cart_items(request):
    if request.user.is_authenticated:
        return Cart.objects.filter(user = request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        return Cart.objects.filter(session_id = request.session.session_key)

def add_to_cart(request, id):
    
    product = Product.objects.get(id = id)
    selected_size = request.POST.get('size')
    quantity = int(request.POST.get('quantity',1))

    user = None
    session_id = None

    if request.user.is_authenticated:
        user = request.user
    else:
        if not request.session.session_key:
            request.session.create()
        session_id = request.session.session_key
   
    if selected_size in product.size_options:
        max_stock = int(product.size_options[selected_size])
        if max_stock > 0:
            cart_item = None
                
            if user:
                cart_item = Cart.objects.filter(user=user, product=product, size=selected_size).first()
            else:
                cart_item = Cart.objects.filter(session_id=session_id, product=product, size=selected_size).first()
            
            if cart_item:
                current_qty_in_cart = cart_item.quantity
                propsed_new_total = current_qty_in_cart + quantity

                if propsed_new_total <= max_stock:
                    cart_item.quantity = propsed_new_total
                    cart_item.save()
                    messages.success(request, f'Updated the cart!')
                else:
                    messages.error(request, f'Cannot add the item anymore in the cart.')
            else:
                if quantity <= max_stock:
                    Cart.objects.create(
                        user=user, 
                        session_id=session_id, 
                        product=product, 
                        size=selected_size, 
                        quantity=quantity
                    )
                    messages.success(request, 'Added to your bag.', extra_tags="cart")
                else:   
                    messages.error(request, f'Only {max_stock} items available.')
        else:
            messages.error(request, f'{selected_size} is out of stock')
    else:
        messages.error(request, 'Invalid size selected')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# def add_to_cart(request, id):
#     cart = Cart(request)
#     product = Product.objects.get(id = id)
#     print("product_id ", id)
#     print("product ", product)
#     selected_size = request.POST.get('size')
#     quantity = int(request.POST.get('quantity', 1))
#     cart.add(product, selected_size, quantity)
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# def my_cart(request):
#     cart = Cart(request)
#     print(cart.cart['1'])
#     total_price = 0
#     delivery_cost = 50
#     item_costs = 0
   
#     if request.method == 'POST':
#         order_id = f'ORDER-{request.user.id}-{datetime.datetime.now().timestamp()}'

#         request.session['order_data']={
#             'name': request.POST['name'],
#             'email' : request.POST['email'],
#             'location': request.POST['location'],
#             'phone': request.POST['phone'],
#             'total_price' : total_price,
#         }
#         payload =   {
#             "return_url": request.build_absolute_uri('khalti-success/'),
#             "website_url": request.build_absolute_uri('/'),
#             "amount": int(total_price * 100),
#             "purchase_order_id": order_id,
#             "purchase_order_name": f'Order by {request.user.username}'
#         }
#         headers = {
#             "Authorization": f"Key {settings.KHALTI_SECRET_KEY}",
#             "Content-Type": "application/json"
#         }
#         try:
#             response = requests.post(settings.KHALTI_INITIATE_URL, json=payload, headers = headers)
#             response_data = response.json()
#             if response.status_code == 200:
#                 return redirect(response_data['payment_url'])
#             else:
#                 error_message = response_data.get('detail', 'An unknown error occurred.')
#                 return render(request, 'merchSite/cart.html', {"error_message": error_message})
#         except requests.exceptions.RequestException as e:
#              return render(request, 'merchSite/cart.html', {"error_message": "Network error, please try again."})
#     return render(request, 'merchSite/cart.html', {"cartitem": cart, "total_price": total_price, "delivery_cost": delivery_cost, "item_costs": item_costs})



def my_cart(request):
    cartitem = get_cart_items(request)
    delivery_cost = 50
    item_costs = sum(item.get_total_cost for item in cartitem)
    total_price = item_costs + delivery_cost
    
    
    if request.method == 'POST':
        order_id = f'ORDER-{request.user.id}-{datetime.datetime.now().timestamp()}'

        request.session['order_data']={
            'name': request.POST['name'],
            'email' : request.POST['email'],
            'location': request.POST['location'],
            'phone': request.POST['phone'],
            'total_price' : total_price,
        }
      

        payload =   {
            "return_url": request.build_absolute_uri('khalti-success/'),
            "website_url": request.build_absolute_uri('/'),
            "amount": int(total_price * 100),
            "purchase_order_id": order_id,
            "purchase_order_name": f'Order by {request.user.username}'
        }
        headers = {
            "Authorization": f"Key {settings.KHALTI_SECRET_KEY}",
            "Content-Type": "application/json"
        }
        try:
            response = requests.post(settings.KHALTI_INITIATE_URL, json=payload, headers = headers)
            response_data = response.json()
            if response.status_code == 200:
                return redirect(response_data['payment_url'])
            else:
                error_message = response_data.get('detail', 'An unknown error occurred.')
                return render(request, 'merchSite/cart.html', {"error_message": error_message})
        except requests.exceptions.RequestException as e:
             return render(request, 'merchSite/cart.html', {"error_message": "Network error, please try again."})
    return render(request, 'merchSite/cart.html', {"cartitem": cartitem, "total_price": total_price, "delivery_cost": delivery_cost, "item_costs": item_costs})


def khalti_success(request):
    cartitem = Cart.objects.filter(user = request.user)
    if request.method == 'GET':
        pidx = request.GET.get('pidx') 
        purchase_order_id = request.GET.get('purchase_order_id')

        payload = {
            "pidx": pidx,
        }
        
        headers = {
            "Authorization": f"Key {settings.KHALTI_SECRET_KEY}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(settings.KHALTI_LOOKUP_URL, json=payload, headers=headers)
            response_data = response.json()
            if response.status_code == 200 and response_data.get('status') == 'Completed':
                order_data = request.session.get('order_data')
                order = Order.objects.create(
                    name= order_data['name'],
                    email = order_data['email'],
                    location = order_data['location'],
                    phone = order_data['phone'],
                    user = request.user,
                    price = order_data['total_price'],
                    order_id = purchase_order_id,
                    transaction_id = response_data.get('transaction_id')
                )
                for cart in cartitem:
                    if cart.product.discount:
                        price = cart.product.discount_price * cart.quantity
                    else:
                        price = cart.product.price * cart.quantity
                    order.add_product(cart.product, cart.size, cart.quantity, price)
                    # cart.product.size_options[cart.size] -= cart.quantity
                    cart.product.save()
            
                Cart.objects.filter(user = request.user).delete()
                order_message = f'New order has been placed by {request.user}, a total of Rs. {price}'
                # send_mail("Order Placed", order_message, settings.EMAIL_HOST_USER, ["ritikshrestha94@gmail.com"], fail_silently=False)
                return render(request, 'merchSite/khalti/khalti-success.html')
            else:
                return redirect('khalti-failure')
        
        except requests.exceptions.RequestException:
            return redirect('khalti-failure')

    return redirect('home')

def khalti_failure(request):
    return render(request, 'merchSite/khalti/khalti-failure.html')

# def my_cart(request):
    
#     cartitem = Cart.objects.filter(user = request.user)
#     total_price = 0
#     delivery_cost = 50
#     item_costs = 0
#     for cart in cartitem:
#         if cart.product.discount:
#             total_price += cart.product.discount_price * cart.quantity
#             item_costs = total_price
#         else:
#             total_price +=cart.product.price * cart.quantity
#             item_costs = total_price

#     total_price += delivery_cost   
#     if cartitem:
#         order_id = f'ORDER-{request.user.id}-{datetime.datetime.now().timestamp()}'
#         secret_key = b"8gBm/:&EnhH.1/q"  # Encode the key to bytes
#         message = f'total_amount={total_price},transaction_uuid={order_id},product_code=EPAYTEST'.encode('utf-8') # Encode the message to bytes
#         hmac_sha256 = hmac.new(secret_key, message, hashlib.sha256)
#         digest = hmac_sha256.digest()
#         signature = base64.b64encode(digest).decode('utf-8')
#         esewa_data = {
#             'amount': total_price,
#             'tax_amount': 0,
#             'service_charge': 0,
#             'delivery_charge': delivery_cost,
#             'total_amount': total_price,
#             'transaction_uuid': order_id,
#             'product_code': 'EPAYTEST',
#             'signature': signature,
            
#             'success_url': request.build_absolute_uri('payment-success/'), 
#             'failure_url': request.build_absolute_uri('payment-failure/'), 
#         }
#         print(esewa_data)
#     else:
#         esewa_data = {} 
     
#     if request.method == 'POST':
       
#         name = request.POST['name']
#         email = request.POST['email']
#         location = request.POST['location']
#         phone = request.POST['phone']
#         order = Order.objects.create(
#             name = name,
#             email = email, 
#             location = location,
#             phone = phone,
#             user = request.user,
#             price = total_price,
#             date = datetime.datetime.now()
#         )
#         for cart in cartitem:
#             if cart.product.discount:
#                 price = cart.product.discount_price * cart.quantity
#             else:
#                 price = cart.product.price * cart.quantity
#             order.add_product(cart.product, cart.size, cart.quantity, price)
#             cart.product.size_options[cart.size] -= cart.quantity
#             cart.product.save()
       
#         Cart.objects.filter(user = request.user).delete()
#         order_message = f'New order has been placed by {request.user}, a total of Rs. {price}'
#         # send_mail("Order Placed", order_message, settings.EMAIL_HOST_USER, ["ritikshrestha94@gmail.com"], fail_silently=False)
#         return redirect('checkout')
#     return render(request, 'merchSite/cart.html', {"cartitem": cartitem, "total_price": total_price, "delivery_cost": delivery_cost, "item_costs": item_costs, "esewa_data": esewa_data})


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
