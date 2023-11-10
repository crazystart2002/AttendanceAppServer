from django.urls import path
from . import views

urlpatterns = [
 path('register_image', views.Register_Image, name='Register_image'),
]