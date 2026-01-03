from . models import Cart


def get_cart_count(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user = request.user).count()
    else:
        if not request.session.session_key:
            return {'cart_count' : 0}
        cart_items = Cart.objects.filter(session_id = request.session.session_key).count()
    return {'cart_count' : cart_items}