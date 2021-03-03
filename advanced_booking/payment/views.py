from django.shortcuts import render, redirect
from .forms import PaymentForm
from django.http import HttpResponse
from movies.models import Movie
from halls.models import Showtime
from .models import Ticket, Order, ShoppingCart


# Create your views here.
def create_new_ticket(seat_id, showtime_id, ticket_type):
    '''
    create a ticket
    '''
    if seat_id and showtime_id and ticket_type:
        # create a new ticket
        new_ticket = Ticket.objects.create(seat_id=seat_id, showtime_id=showtime_id, type=ticket_type)
        return new_ticket


def add_to_cart(seat_id, showtime_id, ticket_type, user):
    '''
    create a ticket and add it to user's shopping cart.
    If current user doesn't have cart, create it first and add ticket to it.

    return true:  if the passing args are valid
    return false : passing args has empty values
    '''
    if seat_id and showtime_id and ticket_type and user:
        # create a new ticket
        new_ticket = create_new_ticket(seat_id, showtime_id, ticket_type)
        if ShoppingCart.objects.filter(user=user).first():
            cart = ShoppingCart.objects.get(user=user)
            cart.ticket.add(new_ticket)
        else:
            cart = ShoppingCart.objects.create(user=user)
            cart.ticket.add(new_ticket)
        cart.save()

        return True
    else:
        print("Can't create a new ticket")
        return False
        # return redirect('index')


def cart(request):
    if request.user.is_authenticated:
        current_user = request.user

        # query the cart
        cart = ShoppingCart.objects.get(user=current_user)

        # FIXME: if front-end just want ticckets in the cart, do:
        tickets = cart.ticket.all()
        # add cart to context
        context = {
            "cart": cart,
            "tickets": tickets
        }
        return render(request, 'cart.html', context)
        # add ticket to context
    else:
        return redirect('index')


def remove_from_cart(user, ticket_id):
    if user.is_authenticated:
        current_user = user
        # query the cart
        cart = ShoppingCart.objects.get(user=current_user)
        ticket = Ticket.objects.get(id=ticket_id)
        cart.ticket.remove(ticket)
        cart.save()
        return True
    else:
        False


def checkout(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid:
            print('payment successful')
            context = {
                'form': form,
                'buttonText': "Pay",
                'action': "",
                'title': "Checkout"
            }
            return render(request, 'form.html', context)
    else:
        form = PaymentForm()
        context = {
            'form': form,
            'buttonText': "Pay",
            'action': "",
            'title': "Checkout"
        }
        return render(request, 'form.html', context)
