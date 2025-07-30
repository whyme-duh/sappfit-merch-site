from django.urls import include, path
from django.conf.urls.static import static
from core import settings
from .views import index, detail_page, add_to_cart, my_cart, delete_cart_item, clear_cart, products_page, checkout, products_by_category

urlpatterns = [
    path('', index, name='home' ),
    path('products/', products_page, name='products' ),
    path('products/<slug:slug>/', detail_page, name='detail-page'),
    path('add-to-cart/<int:id>/', add_to_cart , name='add_to_cart'),
    path('products/category/<int:id>/', products_by_category, name='categories-page'),
    path('my-cart/', my_cart , name= 'my-cart'),
    path('delete-cart-item/<int:id>/', delete_cart_item , name= 'delete-cart-item'),
    path('checkout/', checkout, name='checkout' ),
    path('clear-cart/', clear_cart , name= 'clear-cart'),

] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)