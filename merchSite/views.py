import base64
import hashlib
import hmac
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from core import settings
from merchSite.utils import send_confirmation_email
from . models import Product, Cart,  Order, Categorie, ReturnProduct
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
import random
import datetime
from users.models import Review
from django.db.models import Sum, IntegerField
import requests
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from constance import config
from . forms import TrackOrderForm
from django.db.models.functions import Cast

def error_404_view(request, exception):
    return render(request, 'error/404.html')

def error_500_view(request):
    return render(request, 'error/500.html')


def index(request):
    date = datetime.datetime.now()
    print(date)
    featured_products = Product.objects.filter(discount = True)
    
    
    for product in featured_products:
        available_sizes = [size for size, value in product.size_options.items() if value > 0]
        product.product_available_text = "Available in " + ", ".join(available_sizes) + " sizes" if available_sizes else "No sizes available"
        product.save()
    return render(request, 'merchSite/home.html', {"products" : featured_products, "date":date })

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
    total_stars_count = 0 
    total_rating = len(reviews)
    overall_rating = 0
    product_original_price = product.price
    product_price_with_discount = product.discount_price
    # this is to find the discount rate
    if product_price_with_discount:
        discount_rate = int(((product_original_price-product_price_with_discount)/product_original_price)*100)
    else:
        discount_rate = 0
    
    if reviews:
        for review in reviews:
            total_stars_count += review.review_star
    
        overall_rating = total_stars_count/total_rating

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
    
    return render(request, 'merchSite/product-detail.html', {"product": product, 
        "related_products" : similar_products, 
        'other_products':other_products, 
        "sizes" : sizes, 
        "reviews": reviews, 
        "discount_rate" : discount_rate,
        "overall_rating" : overall_rating,
        "total_rating": total_rating
    })

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
                    messages.success(request, f'Updated your bag! To view it click here!', extra_tags="cart")
                else:
                    messages.error(request, f'Cannot add the item anymore in your bag.')
            else:
                if quantity <= max_stock:
                    Cart.objects.create(
                        user=user, 
                        session_id=session_id, 
                        product=product, 
                        size=selected_size, 
                        quantity=quantity
                    )
                    messages.success(request, 'Added this item to your bag. To view it click here! ', extra_tags="cart")
                else:   
                    messages.error(request, f'Only {max_stock} items available.')
        else:
            messages.error(request, f'{selected_size} is out of stock')
    else:
        messages.error(request, 'Invalid size selected')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# this function is used for "checkout" button on the product page
def direct_checkout_page(request, id):
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
        if max_stock >= quantity:
                
            if user:
                cart_obj, created = Cart.objects.get_or_create(user=user, product=product, size=selected_size, defaults={'quantity' : 0})
            else:
                cart_obj, created = Cart.objects.get_or_create(session_id=session_id, product=product, size=selected_size, defaults={'quantity' : 0})
            
            if created:
                cart_obj.quantity = quantity
            else:
                # this updates the quantity of existing item
                cart_obj.quantity += quantity
            
            cart_obj.save()
        else:
            messages.error(request, f'Only {max_stock} items available.')
    else:
        messages.error(request, 'Invalid size selected')
    
    if user:
        cart_items = Cart.objects.filter(user=user)
    else:
        cart_items = Cart.objects.filter(session_id=session_id)

    if not cart_items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect('products')
    
    total_discounted_price = 0
    total_quantities = 0
    item_costs = 0

    for item in cart_items:
        total_quantities += item.quantity
        
        item_total = item.get_total_cost
        item_costs += item_total
        
        if item.product.discount:
            total_discounted_price += item.get_discounted_price() * item.quantity

    if item_costs >= config.FREE_DELIVERY_THRESHOLD:
        delivery_cost = 0
    else:
        delivery_cost = config.DELIVERY_CHARGE

    total_price = item_costs + delivery_cost
        

    return render(request, 'merchSite/checkoutPage.html', {
                        "cartitem": cart_items, 
                        "total_price": total_price, 
                        "delivery_cost": delivery_cost, 
                        "item_costs": item_costs, 
                        "total_quantities" : total_quantities, 
                        "total_discounted_price" : total_discounted_price
                    })
                

# this function is used by the direct_checkout_page function
# it is the substitute of checkout function and in this we use action to get this function
def place_order(request):
    cartitem = get_cart_items(request)
    if not cartitem:
        messages.success(request, "Redirected to products page with empty cart!")
        return redirect('products')
    total_discounted_price = 0
    total_quantities = 0
    for item in cartitem:
        if item.product.discount:
            total_discounted_price += item.get_discounted_price() * item.quantity
        total_quantities += item.quantity
    item_costs = sum(item.get_total_cost for item in cartitem)
    
    if item_costs >= config.FREE_DELIVERY_THRESHOLD:
        delivery_cost = 0
    else:
        delivery_cost = config.DELIVERY_CHARGE
        
    total_price = item_costs + delivery_cost

    if request.method == 'POST':
        
        if request.user.is_authenticated:
            user_identifier = request.user.id
            user_instance = request.user
        else:
            user_identifier = "GUEST"
            user_instance = None
        
        order_id = f'TEST-ORDER-{user_identifier}-{datetime.datetime.now().timestamp()}'

        try:
            paid = None
            payment_option = request.POST['payment']
            if payment_option == "Cash On Delivery":
                paid = False
            order = Order.objects.create(
                name=request.POST['name'],
                email=request.POST['email'],
                location=request.POST['location'],
                phone=request.POST['phone'],
                user=user_instance, 
                price=total_price,
                order_id=order_id,
                transaction_id="MANUAL-TEST-MODE",
                is_paid = paid,
                payment_option = payment_option
            )

            for cart in cartitem:
                if cart.product.discount:
                    price = cart.product.discount_price * cart.quantity
                else:
                    price = cart.product.price * cart.quantity
                order.add_product(cart.product, cart.size, cart.quantity, price)

            # send_confirmation_email(order)
            messages.success(request, f"Order placed successfully! (ID: {order.id})")
            cartitem.delete()

            return render(request, 'merchSite/khalti/khalti-success.html', {'order_id' : order_id}) 

        except Exception as e:
            print(f"Error creating order: {e}")
            messages.error(request, "Something went wrong creating the order.")
            return redirect('checkout')
        

def cancel_order(request, id):
    order = Order.objects.get(id = id)
    if request.method == "POST":
        if order.status == "Delivered" or order.status == "Shipped" or order.status == "Returned":
            messages.error(request, f"Since the product has been {order.status}, you can't cancel the product.")
        else:
            cancellation_reason_choice = request.POST.get('cancel-options')
            cancellation_other_reason = request.POST.get('reason')
            order.status = "Cancelled"
            order.cancellation_reasons = cancellation_reason_choice
            order.cancellation_other_reason = cancellation_other_reason
            order.save()
            messages.success(request, f'Your Order has been cancelled succesfully!')
            return redirect('profile')
    return redirect('profile')
    

def my_cart(request):
    cartitem = get_cart_items(request)
    total_discounted_price = 0
    total_quantities = 0
    for item in cartitem:
        if item.product.discount:
            total_discounted_price += item.get_discounted_price() * item.quantity
        total_quantities += item.quantity
        max_stock = int(item.product.size_options[item.size])
        if max_stock < item.quantity:
            item.delete()
            messages.error(request, f'The item is not available!')
    item_costs = sum(item.get_total_cost for item in cartitem)
    if item_costs >= config.FREE_DELIVERY_THRESHOLD:
        delivery_cost = 0
    else:
        delivery_cost = config.DELIVERY_CHARGE
    total_price = item_costs + delivery_cost

    return render(request, 'merchSite/cart.html', {"cartitem": cartitem, "total_price": total_price, "delivery_cost": delivery_cost, "item_costs": item_costs, "total_quantities" : total_quantities, "total_discounted_price" : total_discounted_price})

@never_cache
def checkout(request):
    cartitem = get_cart_items(request)
    if not cartitem:
        messages.success(request, "Redirected to products page with empty cart!")
        return redirect('products')
    total_discounted_price = 0
    total_quantities = 0
    for item in cartitem:
        if item.product.discount:
            total_discounted_price += item.get_discounted_price() * item.quantity
        total_quantities += item.quantity
    item_costs = sum(item.get_total_cost for item in cartitem)
    
    if item_costs >= config.FREE_DELIVERY_THRESHOLD:
        delivery_cost = 0
    else:
        delivery_cost = config.DELIVERY_CHARGE
        
    total_price = item_costs + delivery_cost

    if request.method == 'POST':
        
        if request.user.is_authenticated:
            user_identifier = request.user.id
            user_instance = request.user
        else:
            user_identifier = "GUEST"
            user_instance = None
        
        order_id = f'TEST-ORDER-{user_identifier}-{datetime.datetime.now().timestamp()}'

        try:
            paid = None
            payment_option = request.POST['payment']
            if payment_option == "Cash On Delivery":
                paid = False
            order = Order.objects.create(
                name=request.POST['name'],
                email=request.POST['email'],
                location=request.POST['location'],
                phone=request.POST['phone'],
                user=user_instance, 
                price=total_price,
                order_id=order_id,
                transaction_id="MANUAL-TEST-MODE",
                is_paid = paid,
                payment_option = payment_option
            )

            for cart in cartitem:
                if cart.product.discount:
                    price = cart.product.discount_price * cart.quantity
                else:
                    price = cart.product.price * cart.quantity
                order.add_product(cart.product, cart.size, cart.quantity, price)
                cart.product.size_options[cart.size] -= cart.quantity
                cart.product.save()

            # send_confirmation_email(order)
            messages.success(request, f"Order placed successfully! (ID: {order.id})")
            cartitem.delete()

            return render(request, 'merchSite/khalti/khalti-success.html', {'order_id' : order_id}) 

        except Exception as e:
            print(f"Error creating order: {e}")
            messages.error(request, "Something went wrong creating the order.")
            return redirect('checkout')

    return render(request, 'merchSite/checkoutPage.html', {
        "cartitem": cartitem, 
        "total_price": total_price, 
        "delivery_cost": delivery_cost, 
        "item_costs": item_costs, 
        "total_quantities": total_quantities, 
        "total_discounted_price": total_discounted_price
    })
    
    
        

# def checkout(request):
#     cartitem = get_cart_items(request)
#     total_discounted_price = 0
#     total_quantities = 0
#     for item in cartitem:
#         if item.product.discount:
#             total_discounted_price += item.get_discounted_price() * item.quantity

#         total_quantities += item.quantity
#     if cartitem:
#         item_costs = sum(item.get_total_cost for item in cartitem)
#         if item_costs >= config.FREE_DELIVERY_THRESHOLD:
#             delivery_cost = 0
#         else:
#             delivery_cost = config.DELIVERY_CHARGE
#         total_price = item_costs + delivery_cost
#         if request.method == 'POST':
#             if request.user.is_authenticated:
#                 user_identifier = request.user.id
#             else:
#                 user_identifier = f'{request.POST['name']} + GUEST'
#             order_id = f'ORDER-{user_identifier}-{datetime.datetime.now().timestamp()}'

#             request.session['order_data']={
#                 'name': request.POST['name'],
#                 'email' : request.POST['email'],
#                 'location': request.POST['location'],
#                 'phone': request.POST['phone'],
#                 'total_price' : total_price,
#             }
#             purchase_name = request.POST['name']
            

#             payload =   {
#                 "return_url": request.build_absolute_uri('khalti-success/'),
#                 "website_url": request.build_absolute_uri('/'),
#                 "amount": int(total_price * 100),
#                 "purchase_order_id": order_id,
#                 "purchase_order_name": f'Order by {purchase_name}'
#             }
#             headers = {
#                 "Authorization": f"Key {settings.KHALTI_SECRET_KEY}",
#                 "Content-Type": "application/json"
#             }
#             try:
#                 response = requests.post(settings.KHALTI_INITIATE_URL, json=payload, headers = headers)
#                 response_data = response.json()
#                 if response.status_code == 200:
#                     return redirect(response_data['payment_url'])
#                 else:
#                     error_message = response_data.get('detail', 'An unknown error occurred.')
#                     return render(request, 'merchSite/cart.html', {"error_message": error_message})
#             except requests.exceptions.RequestException as e:
#                 return render(request, 'merchSite/cart.html', {"error_message": "Network error, please try again."})
#         return render(request, 'merchSite/checkoutPage.html',  {"cartitem": cartitem, "total_price": total_price, "delivery_cost": delivery_cost, "item_costs": item_costs, "total_quantities" : total_quantities, "total_discounted_price" : total_discounted_price})
#     else:
#         messages.success(request, "Redirected to Products page since your bag is empty.")
#         return redirect('products')
        

def khalti_success(request):
    cartitem = get_cart_items(request)
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
                user_instance = request.user if request.user.is_authenticated else None
                order = Order.objects.create(
                    name= order_data['name'],
                    email = order_data['email'],
                    location = order_data['location'],
                    phone = order_data['phone'],
                    user = user_instance,
                    price = order_data['total_price'],
                    order_id = purchase_order_id,
                    transaction_id = response_data.get('transaction_id')
                )
                final_price = 0
                for cart in cartitem:
                    if cart.product.discount:
                        price = cart.product.discount_price * cart.quantity
                    else:
                        price = cart.product.price * cart.quantity
                    order.add_product(cart.product, cart.size, cart.quantity, price)
                    # cart.product.size_options[cart.size] -= cart.quantity
                    cart.product.save()
                    final_price += price
            
                cartitem.delete()
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


def delete_cart_item(request, id):
    try:
        if request.user.is_authenticated:
            cart_item = Cart.objects.get(id = id, user = request.user)
        else:
            cart_item = Cart.objects.get(id = id, session_id = request.session.session_key)
        cart_item.delete()
    except Exception as e:
        print(e)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def clear_cart(request):
    if request.user.is_authenticated:
        cart_item = Cart.objects.filter(user = request.user)
    else:
        cart_item = Cart.objects.filter(session_id = request.session.session_key)
    cart_item.delete()
    messages.success(request, f'Deleted the cart items successfully!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 



def track_order(request):
    order_products = []
    
    if request.method == 'POST':
        track_order_form = TrackOrderForm(request.POST)
        if track_order_form.is_valid():
            email = request.POST.get('email', '').strip()
            order_id = request.POST.get('order_id', '').strip()
            order_items = Order.objects.filter( email = email, order_id = order_id)
            if not order_items:
                messages.error(request, f'The provided detail are incorrect!')
            else:
                for order in order_items:
                    if order.product: 
                        products = json.loads(order.product) 
                        for i in range(len(products)):
                            product_obj = Product.objects.get(id = products[i]['id'])
                            products[i]['product_slug'] = product_obj.slug
                            products[i]['product_img_url'] = product_obj.image.url
                        order_products.append({
                            'order': order,
                            'products': products
                        })
            
              
    else:
        track_order_form = TrackOrderForm()
    return render(request, 'merchSite/track_order.html', {'form': track_order_form, 'order_products': order_products})



def return_request(request, order_id):
    order = get_object_or_404(Order, id = order_id)
    return_elligible = None
    now_date = datetime.datetime.now()
    delivered_date = order.delivered_date
    if delivered_date.year == now_date.year and delivered_date.month == now_date.month:
        if delivered_date.day - now_date.day > 7:
            return_elligible = False
        else:
            return_elligible = True
    if return_elligible:
        if request.user.is_authenticated and request.method == "POST":
            product_name = request.POST.get('product-name')
            size = request.POST.get('product-size')
            try:
                requested_quantity = int(request.POST.get('product-quantity', 0))
            except (ValueError, TypeError):
                messages.error(request, "Invalid quantity provided.")
                return redirect('prpfile')
            
            original_qty_bought = 0
            item_found = False

            try:
                order_items = json.loads(order.product)

                for item in order_items:
                    if item.get('product') == product_name  and item.get('size') == size:
                        original_qty_bought = int(item.get('quantity', 0))
                        item_found = True
                        break
                
            except json.JSONDecodeError:
                messages.error(request, "System error!")
                return redirect('profile')
            
            if not item_found:
                messages.error(request, "The item was not found in your order")
                return redirect('profile')


            previous_returns_sum = ReturnProduct.objects.filter(
                        order=order,
                        product__name=product_name, 
                        size=size
                    ).aggregate(total=Sum(Cast('quantity', output_field = IntegerField())))['total'] or 0
            max_returnable = original_qty_bought - previous_returns_sum
            if requested_quantity <= 0:
                messages.error(request, "Return quantity should be greater than 0")
                return redirect('profile')
            elif requested_quantity > max_returnable:
                messages.error(request, f"Error! You've bought {original_qty_bought} units of this item.")
                return redirect('profile')
            else:
                try:
                    product_instance = Product.objects.get(name = product_name)

                    ReturnProduct.objects.create(
                        user = request.user, 
                        product = product_instance, 
                        size = size, 
                        quantity = requested_quantity, 
                        order = order, 
                    )
                    
                    messages.success(request, f'Your return request has been submitted!')
                except Product.DoesNotExist:
                    messages.error(request, 'Product details mismatch!')
                except Exception as e:
                    messages.error(request, f'There was an error! {e}')
    else:
        messages.error(request, 'The delivererd product is already 7 days old!')
    return redirect('profile')
    

    