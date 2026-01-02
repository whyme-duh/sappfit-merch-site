from . models import Cart


def merge_cart(old_session_key, user):
    guest_cart_items = Cart.objects.filter(session_id = old_session_key)

    if guest_cart_items.exists():
        for guest_item in guest_cart_items:
            existing_user_item = Cart.objects.filter(user = user, product = guest_item.product, size = guest_item.size).first()

            if existing_user_item:
                print("hi")
                existing_user_item.quantity += guest_item.quantity
                existing_user_item.save()
                guest_item.delete()
            else:
                guest_item.user = user
                guest_item.session_id = None
                guest_item.save()