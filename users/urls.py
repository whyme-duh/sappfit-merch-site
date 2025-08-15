from django.urls import path
from . views import profile, sign_up, review_page, add_review
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("profile/", profile, name= "profile"),
    path('sign-up/', sign_up, name='sign-up' ),
    path('review/', review_page, name = 'review' ),
    path('add-review/<int:id>/', add_review, name = 'add-review' ),
  
]