from django.urls import path
from . views import profile, sign_up, review_page, edit_review, delete_review, add_review, ResetPasswordView, cancel_order
from django.contrib.auth import views as auth_views



urlpatterns = [
    path("profile/", profile, name= "profile"),
    path('sign-up/', sign_up, name='sign-up' ),
    path('review/', review_page, name = 'review' ),
    path('add-review/<int:id>/', add_review, name = 'add-review' ),
    path('password-reset/', ResetPasswordView.as_view(), name = 'password-reset' ),
    path('cancel-order/<int:id>/', cancel_order, name = 'cancel-order' ),
    path('delete-review/<int:id>/', delete_review, name = 'delete-review' ),
    path('edit-review/<int:id>/', edit_review, name = 'edit-review' ),
  
]