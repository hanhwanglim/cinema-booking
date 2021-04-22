from django.urls import path

from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('booking', views.booking, name='booking'),
    path('booking/resend_ticket/<int:order_id>', views.resend_ticket, name='resend_ticket'),
    path('verify/<auth_token>', views.verify, name='verify')
]
