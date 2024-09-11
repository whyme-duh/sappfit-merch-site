from django.urls import include, path
from django.conf.urls.static import static
from core import settings
from .views import index, detail_page, add_to_cart, my_cart

urlpatterns = [
    path('', index, name='home' ),
    path('products/<slug:slug>/', detail_page, name='detail-page'),
    path('add-to-cart/<int:id>/', add_to_cart , name='add_to_cart'),
    path('my-cart/', my_cart , name= 'my-cart'),

] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)