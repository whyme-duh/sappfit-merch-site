from django.urls import include, path
from django.conf.urls.static import static
from core import settings
from .views import index, sign_up

urlpatterns = [
    path('', index, name='home' ),
    path('sign-up/', sign_up, name='sign-up' )

] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)