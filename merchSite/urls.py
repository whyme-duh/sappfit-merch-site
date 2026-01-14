from django.urls import include, path
from django.conf.urls.static import static
from core import settings
from .views import index, return_request, detail_page, add_to_cart, track_order, my_cart, delete_cart_item, clear_cart, products_page, checkout, products_by_category, product_filter, product_filter_along_with_category, khalti_failure, khalti_success

urlpatterns = [
    path('', index, name='home' ),
    path('products/', products_page, name='products' ),
    path('products/filters/<str:filter>/', product_filter, name='products-filter' ),
    path('products/category/filters/<int:id>/<str:filter>/', product_filter_along_with_category, name='products-filter-category' ),
    path('products/<slug:slug>/', detail_page, name='detail-page'),
    path('add-to-cart/<int:id>/', add_to_cart , name='add_to_cart'),
    path('products/category/<int:id>/', products_by_category, name='categories-page'),
    path('my-cart/', my_cart , name= 'my-cart'),
    path('delete-cart-item/<int:id>/', delete_cart_item , name= 'delete-cart-item'),
    path('checkout/', checkout, name='checkout' ),
    path('clear-cart/', clear_cart , name= 'clear-cart'),
    path('return-product/<int:order_id>/', return_request , name= 'return-product'),
    path('my-cart/khalti-success/', khalti_success, name='khalti-success'),
    path('my-cart/khalti-failure/', khalti_failure, name='khalti-failure'),
    path('track-order/', track_order, name='track-order'),

] 