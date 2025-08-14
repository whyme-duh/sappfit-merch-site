from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . forms import UserRegistrationForm
from merchSite.models import Order
from django.contrib.auth.models import User
import json

@login_required
def profile(request):
    orders = Order.objects.filter(user=request.user).order_by('-date')
    order_products = []

    for order in orders:
        if order.product: 
            products = json.loads(order.product) 
            print(products[0])
            order_products.append({
                'order': order,
                'products': products
            })
    return render(request, 'users/profile.html', {"order_products": order_products})

def sign_up(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/signup.html', {'form': form})