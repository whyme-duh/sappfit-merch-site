import json

import json

from django.utils import timezone
import datetime
from django.db.models import Sum
from django.shortcuts import redirect, render

from merchSite.models import User, Product, Order

def custom_admin_view(request):
    if request.user.is_superuser or request.user.is_staff:
        total_income = Order.objects.filter(status="Delivered").aggregate(Sum('price'))['price__sum'] or 0
        total_sales = Order.objects.filter(status = "Delivered").count()
        pending_order = Order.objects.filter(status = "Pending")
        pending_order_count = pending_order.count()
        current_month = timezone.now().month
        products = Product.objects.filter(total_quantity__lt = 2)
        out_of_stock_products  = Product.objects.filter(total_quantity = 0)
        pending_orders_offload = []
        for order in pending_order:
            try:
                product_list = json.loads(order.product)
                pending_orders_offload.append({
                    'order' : order,
                    'products' : product_list
                })
            except json.JSONDecodeError:
                continue

        current_month_name = datetime.datetime.now().strftime("%B")
        
        monthly_sales = Order.objects.filter(date__month = current_month, status = "Delivered").aggregate(Sum('price'))['price__sum'] or 0
        context = {
            "total_income" : total_income,
            "total_sales" : total_sales,
            "current_month_name" : current_month_name,
            "monthly_sales" : monthly_sales,
            "products" : products,
            "out_of_stock_products": out_of_stock_products,
            "pending_order_count": pending_order_count,
            "pending_orders_offload":  pending_orders_offload
        }
        return render(request, 'merchSite/custom_admin/custom_admin.html', context = context)
    return redirect('home')
