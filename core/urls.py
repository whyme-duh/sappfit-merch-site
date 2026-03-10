"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from . import settings
from django.contrib.auth import views as auth_views
from users.views import CustomLoginView
import django_browser_reload

admin.site.site_header = "Sappfit Merch Site"
admin.site.site_title = "Admin Site | Sappfit Merch"
admin.site.index_title = "Welcome"

urlpatterns = [
    path('__reload__/', include("django_browser_reload.urls")),
    path('admin/', admin.site.urls, name = 'admin'),
    path('', include('merchSite.urls')),
    path('users/', include('users.urls')),
    path('login/',CustomLoginView.as_view(template_name = 'users/login.html', redirect_authenticated_user= True), name = 'login'),
    path('logout/',auth_views.LogoutView.as_view(template_name = 'users/login.html'), name = 'logout'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name= 'users/passwordReset/password_reset_confirm.html'), name='password-reset-confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/passwordReset/password_reset_complete.html'), name='password_reset_complete'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


