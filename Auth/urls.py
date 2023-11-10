from django.urls import path
from . import views

urlpatterns = [
    path('register', views.UserRegistrationView.as_view(), name='Register'),
    path('login', views.UserLoginView.as_view(), name='Login'),
    path('profile', views.UserProfileView.as_view(), name='Profile'),
    path('image_register/<str:pk>', views.image_confirmation, name="Confirmation_Image")
]
