from django.urls import path

from . import views

urlpatterns = [
    path('cart/checkout',views.payment, name='checkout')
]