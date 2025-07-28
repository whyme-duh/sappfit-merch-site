from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . forms import UserRegistrationForm
from merchSite.models import Order
from django.contrib.auth.models import User

@login_required
def profile(request):
    orders = Order.objects.filter(user = request.user)
    return render(request, 'users/profile.html', {"orders" : orders})

def sign_up(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/signup.html', {'form': form})