from django.shortcuts import render
from .cart import Cart
from .models import Ticket

# Create your views here.

#TODO:display the cart page
# def cart_page(request):
#     cart = Cart(request)
#
#     return render(request, cart, '/cart/cart.html')

#TODO:add a ticket to cart
# def add_to_cart(request,ticket_id):
#
#         #TODO:create a ticket by using the form
#
#
#         #TODO:add the ticket to cart
#         cart = Cart(request)
#         cart.add(ticket)
#
#         return render('/')
