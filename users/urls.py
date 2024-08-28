from django.urls import path
from . views import profile, sign_up
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("profile/", profile, name= "profile"),
    path('sign-up/', sign_up, name='sign-up' )

  
]