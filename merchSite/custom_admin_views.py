from django.utils import timezone
import datetime
from django.db.models import Sum
from django.shortcuts import redirect, render

from merchSite.models import User, Product, Order

def custom_admin_view(request):
    if request.user.is_superuser:
        total_income = Order.objects.filter(status="Delivered").aggregate(Sum('price'))['price__sum'] or 0
        total_sales = Order.objects.filter(status = "Delivered").count()
        pending_order = Order.objects.filter(status = "Pending").count()
        current_month = timezone.now().month
        products = Product.objects.all()
        out_of_stock_products = []
        for product in products:
            available_size = [size for size, value in product.size_options.items() if value > 0]
            available_size_text = "Avilable" if available_size else "Out of Stock"
            if available_size_text == "Out of Stock":
                out_of_stock_products.append(product.name)
        current_month_name = datetime.datetime.now().strftime("%B")
        
        monthly_sales = Order.objects.filter(date__month = current_month, status = "Delivered").aggregate(Sum('price'))['price__sum'] or 0
        context = {
            "total_income" : total_income,
            "pending_order" : pending_order,
            "total_sales" : total_sales,
            "current_month_name" : current_month_name,
            "monthly_sales" : monthly_sales,
            "out_of_stock_products": out_of_stock_products
            
        }
        return render(request, 'merchSite/custom_admin/custom_admin.html', context = context)
    return redirect('home')
