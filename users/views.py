from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . forms import UserRegistrationForm, ReviewForm
from merchSite.models import Order, Product
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
    subject_template_name = 'users/passwordReset/password_rest_subject.txt'
    success_message =  "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('home')


@login_required
def profile(request):
    reviews = Review.objects.filter(user = request.user)
    orders = Order.objects.filter(user=request.user).order_by('-date')
    order_products = []

    for order in orders:
        if order.product: 
            products = json.loads(order.product) 
            order_products.append({
                'order': order,
                'products': products
            })
    return render(request, 'users/profile.html', {"order_products": order_products, 'reviews' : reviews})

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
    orders = Order.objects.filter(user = request.user, delivered=True)
    delivered_products_list = []
    for order in orders:
        if order.product: 
            products = json.loads(order.product) 
            for item in products:
                delivered_products_list.append(item)
    return render(request, 'users/review.html', {'delivered_products': delivered_products_list, "reviews": reviews})

@login_required
def add_review(request, id):
    orders = Order.objects.filter(user = request.user, delivered=True)
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


# class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
#     template_name = "users/password_reset.html"
#     email_template_name = "users/password_email_reset.html"
#     subject_template_name = "users/password_reset_subject"
#     success_message = "We've emailed you instructions for setting your password, " \
#                       "if an account exists with the email you entered. You should receive them shortly." \
#                       " If you don't receive an email, " \
#                       "please make sure you've entered the address you registered with, and check your spam folder."
#     success_url = reverse_lazy()
