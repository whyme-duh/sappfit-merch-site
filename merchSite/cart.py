from decimal import Decimal
from core import settings
from merchSite.models import Product 


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart



    def add(self, product, size, quantity = 1, override_quantity = False):
        product_id = str(product.id)
        quantity = int(quantity)
        
        if product.discount:
            price_to_store = str(product.discount_price)
        else:
            price_to_store = str(product.price)
        self.cart[product_id] = {
            'quantity' : quantity,
            'size' : size,
            'price': price_to_store
        }        
        self.save()

    def remove(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in = product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(int(item['quantity']) for item in self.cart.values())
    
    def get_sub_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item
            in self.cart.values())
    
    def clear(self):
        self.cart.clear()
        self.save()

    def save(self):
        self.session.modified = True
        