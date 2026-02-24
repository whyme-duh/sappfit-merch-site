from django.db.models import Sum, Count
from django.utils import timezone
import datetime
from merchSite.models import Order, Product


def dashboard_callback(request, context):
    total_income = Order.objects.filter(status="Delivered").aggregate(Sum('price'))['price__sum'] or 0
    total_order = Order.objects.filter(status = "Delivered").count()
    pending_order = Order.objects.filter(status = "Pending").count()
    cancelled_order = Order.objects.filter(status = "Cancelled").count()
    returned_order = Order.objects.filter(status = "Returned").count()
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

    context.update({
        "kpi": [
             {
                "title": "Out Of Stock Products",
                "metric": out_of_stock_products,
                "color": "primary"
            },
            
            {
                "title": "Total Revenue",
                "metric": f"Rs. {total_income}",
                "footer" : "Lifetime earnings",
                "color": "primary"
            },
            {
                "title": "Monthly Sales",
                "metric": f"Rs. {monthly_sales}",
                "footer" : f"Of {current_month_name}",
                "color": "success"
            },
            {
                "title": "Pending Orders",
                "metric": f"{pending_order}",
                "footer" : "Need Attention ",
                "color": "warning"
            },
            {
                "title": "Total Orders Delivered",
                "metric": f"{total_order}",
                "footer" : "All time ",
                "color": "info"
            },
            {
                "title": "Total Cancelled Order",
                "metric": f"{cancelled_order}",
                "footer" : "All time ",
                "color": "info"
            },
            {
                "title": "Total Returned Order",
                "metric": f"{returned_order}",
                "footer" : "All time ",
                "color": "info"
            },
            
        ]
    })
   
    return context