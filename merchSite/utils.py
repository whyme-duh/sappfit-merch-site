import json
from core import settings
from . models import Cart

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# this function is created in order to merge the cart item of a guest account
# if the guest account (anonymous account) has items on its cart, then the cart will be updated once the user logs in

def merge_cart(old_session_key, user):
    guest_cart_items = Cart.objects.filter(session_id = old_session_key)

    if guest_cart_items.exists():
        for guest_item in guest_cart_items:
            existing_user_item = Cart.objects.filter(user = user, product = guest_item.product, size = guest_item.size).first()

            if existing_user_item:
                existing_user_item.quantity += guest_item.quantity
                existing_user_item.save()
                guest_item.delete()
            else:
                guest_item.user = user
                guest_item.session_id = None
                guest_item.save()



def send_confirmation_email(order):
    order_products = []
    product_list = json.loads(order.product)
    
    subject = f'Order Confirmation - {order.order_id}'
    to_email = order.email  
    from_email = settings.EMAIL_HOST_USER

    context = {
        'order': order,
        'product_list' : product_list,
        'domain': "http://127.0.0.1:8000/"
    }

    html_content = render_to_string('merchSite/email/order_success.html', context)
    
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    email.attach_alternative(html_content, "text/html")
    
    try:
        email.send()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")


    