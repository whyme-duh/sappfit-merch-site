from django.db.models import Sum, Count
from django.utils import timezone
import datetime
from merchSite.models import Order


def dashboard_callback(request, context):
    total_income = Order.objects.filter(status="Delivered").aggregate(Sum('price'))['price__sum'] or 0
    total_order = Order.objects.filter(status = "Delivered").count()
    pending_order = Order.objects.filter(status = "Pending").count()
    current_month = timezone.now().month

    current_month_name = datetime.datetime.now().strftime("%B")
    
    monthly_sales = Order.objects.filter(date__month = current_month, status = "Delivered").aggregate(Sum('price'))['price__sum'] or 0

    context.update({
        "kpi": [
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
                "metric": f"Rs. {pending_order}",
                "footer" : "Need Attention ",
                "color": "warning"
            },
            {
                "title": "Total Orders",
                "metric": f"Rs. {total_order}",
                "footer" : "All time ",
                "color": "info"
            },
            
        ]
    })
   
    return context