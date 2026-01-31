from collections import defaultdict
import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from . forms import UserRegistrationForm, ReviewForm
from merchSite.models import Order, Product, ReturnProduct
from django.contrib.auth.models import User
from . models import Review
from django.contrib import messages
import json
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView
from merchSite.utils import merge_cart


class CustomLoginView(LoginView):
    template_name = "users/login.html"

    def form_valid(self, form):
        old_session_key = self.request.session.session_key
        response = super().form_valid(form)
        if old_session_key:
            merge_cart(old_session_key, self.request.user)
        return response
    
class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/passwordReset/password_reset.html'
    email_template_name = 'users/passwordReset/password_reset_email.html'
    subject_template_name = 'users/passwordReset/password_reset_subject.txt'
    success_message =  "We've emailed you instructions for setting your password, "\
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('home')


@login_required
def profile(request):
    reviews = Review.objects.filter(user = request.user)
    orders = Order.objects.filter(user=request.user).order_by('-date')
    returned_products = ReturnProduct.objects.filter(user = request.user)
    now_date = datetime.datetime.now()

    # creating a dictionary that stores the product name and size
    returns_map = defaultdict(int)

    returned_products_list = []

    for return_prod in returned_products:
        key = (return_prod.product.name, return_prod.size)
        returns_map[key] += int(return_prod.quantity)
        returned_products_list.append(return_prod)

    order_products = []
    delivered_products = []


    for order in orders:
        ordered_date = order.date
        if not order.product:
            continue
        try:
            products_list = json.loads(order.product) 
            order_products.append({
                'order': order,
                'products': products_list
            })
            if order.status == "Delivered":
                for item in products_list:
                    product_name = item.get('product')
                    product_size = item.get('size')
                    product_quantity = int(item.get('quantity', 0))
                    
                    item_key = (product_name, product_size)

                    # this code below helps to check whether the delivered product
                    # is eligible for returning or not

                    if not item.get('returning_eligible'):
                        if ordered_date.year == now_date.year and ordered_date.month == now_date.month:
                            if ordered_date.day - now_date.day > 7:
                                item['returning_eligible'] = False
                            else:
                                item['returning_eligible'] = True

                    quantity_returned = returns_map.get(item_key, 0)
                    
                    if quantity_returned > 0:
                        remaining_qty = product_quantity - quantity_returned

                        if remaining_qty > 0:
                            item_copy = item.copy()
                            item_copy['quantity'] = remaining_qty
                            delivered_products.append(item_copy)

                            returns_map[item_key] = 0
                        else:
                            returns_map[item_key] -= product_quantity
                    else:
                        delivered_products.append(item)

                   
        except json.JSONDecodeError:
            continue
    context = {"order_products": order_products, 
            'reviews' : reviews, 
            'delivered_products' : delivered_products, 
            'returned_products' : returned_products_list}

  
    return render(request, 'users/profile.html', context)

def sign_up(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/signup.html', {'form': form})

@login_required
def review_page(request):
    reviews = Review.objects.filter(user = request.user)
    orders = Order.objects.filter(user = request.user, status ="Delivered")
    delivered_products_list = []
    for order in orders:
        if order.product: 
            products = json.loads(order.product) 
            for item in products:
                delivered_products_list.append(item)
    return render(request, 'users/review.html', {'delivered_products': delivered_products_list, "reviews": reviews})

def cancel_order(request, id):
  
    order = Order.objects.get(id = id)
    if order.status == "Delivered" or order.status == "Shipped":
        messages.error(request, f"Since the product has been {order.status}, you can't cancel the product.")
    else:
        if request.method == "POST":
            cancellation_reason_choice = request.POST.get('cancel-options')
            canellation_other_reason = request.POST.get('reason')
            order.status = "Cancelled"
            order.cancellation_reasons = cancellation_reason_choice
            order.cancellation_other_reason = canellation_other_reason
            order.save()
            messages.success(request, f'Your Order has been cancelled succesfully!')
    return redirect('profile')



@login_required
def add_review(request, id):
    orders = Order.objects.filter(user = request.user, status ="Delivered")
    product = Product.objects.get(id = id)
    existing_review = Review.objects.filter(user = request.user, product = product).first()
    if existing_review:
        messages.warning(request, "You have already reviewed this product")
        return redirect('profile')
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        
        if form.is_valid():
            review_star = form.cleaned_data['review_star']
            review = form.cleaned_data['review']
            for order in orders:
                if order.product: 
                    products = json.loads(order.product) 
                    for item in products:
                        if item["id"] == id:
                            item["reviewed"] = True
                    order.product = json.dumps(products)
                    order.save()
            Review.objects.create(review = review, review_star = review_star, user = request.user, product = product)
            messages.success(request, f'Review added successfully. Thank you!')
            return redirect('profile')
        else:
            form = ReviewForm()
    return render(request, 'users/addReview.html', {'form': form, 'product' : product})


def delete_review(request, id):
    review = get_object_or_404(Review, id = id, user= request.user)
    if review:
        review.delete()
        messages.success(request, "Deleted your review!")
        return redirect('profile')
    else:
        messages.error(request, "Something went wrong. Try Again!")
        return redirect('profile')
    

def edit_review(request, id):
    review = get_object_or_404(Review, id = id, user= request.user)
    old_review_star = review.review_star
    product = review.product
    old_review = review.review
    form = ReviewForm(request.POST)

    if review:
        if request.method == 'POST':
            form = ReviewForm(request.POST)
            if form.is_valid():
                review_star_update = form.cleaned_data['review_star']
                review_update = form.cleaned_data['review']
                
                review.review = review_update
                review.review_star = review_star_update
                review.save()
                messages.success(request, f'Updated your review!')
                return redirect('profile')
            else:
                form = ReviewForm()
        return render(request, 'users/editReview.html', {'form': form, 'old_review': old_review, 'old_review_star' : old_review_star, 'product': product})
        
    else:
        messages.error(request, "Something went wrong. Try Again!")
        return redirect('profile')