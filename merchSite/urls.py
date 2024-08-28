from django.urls import include, path
from django.conf.urls.static import static
from core import settings
from .views import index, detail_page

urlpatterns = [
    path('', index, name='home' ),
    path('products/<slug:slug>/', detail_page, name='detail-page'),

] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)