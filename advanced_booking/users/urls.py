from django.urls import path

from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('booking', views.booking, name='booking')
]