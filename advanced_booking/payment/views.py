from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .forms import CardForm
from movies.models import Movie
from halls.models import Showtime
from .models import Ticket, Order, ShoppingCart, CardDetail
from .create_ticket_image import ticket_info, generate_ticket

# adjust discount for each type here.
ticket_value = {'CHILD': 50, 'ADULT': 50, 'SENIOR': 50 * 0.8}  # map ticket type to ticket values


def create_new_ticket(seat_id, showtime_id, ticket_type):
    """
    create a ticket
    """
    if seat_id and showtime_id and ticket_type:
        # create a new ticket
        # print("ticket_type is:")
        # print(ticket_type)
        new_ticket = Ticket.objects.create(seat_id=seat_id, showtime_id=showtime_id, type=ticket_type)
        return new_ticket


# cart functions  #
def add_to_cart(request, seat_id, showtime_id, ticket_type):
    """
    create a ticket and add it to user's shopping cart.
    If current user doesn't have cart, create it first and add ticket to it.

    return to the cart page
    """

    if request.user.is_authenticated:
        if seat_id and showtime_id and ticket_type:
            # create a new ticket
            # print("ticket_type is:")
            # print(ticket_type)
            # FIXME: elegant way to limit this.
            # Limit buying child ticket for movies which are 18 OR R18 in certificate.
            if ticket_type == 'CHILD':
                if  Showtime.objects.get(id=showtime_id).movie.certificate in ["18", "R18"]:
                    messages.add_message(request, messages.error, "Movie certificate Limitation:"
                                                                  " can't buy for child")
                    print("Error:Movie Rating Limitation")
                    return redirect('index')

            new_ticket = create_new_ticket(seat_id, showtime_id, ticket_type)
            if ShoppingCart.objects.filter(user=request.user).first():
                cart = ShoppingCart.objects.get(user=request.user)
                cart.ticket.add(new_ticket)
            else:
                cart = ShoppingCart.objects.create(user=request.user)
                cart.ticket.add(new_ticket)
            cart.save()
            return redirect('cart')
        else:
            messages.add_message(request, messages.error, "Can't create ticket"
                                                          " due to null values")
            print("Error: Can't create ticket due to null values")
            return redirect('index')
    else:
        messages.add_message(request, messages.error, "Unauthenticated user!")
        print("Error: Unauthenticated user!")
        return redirect('index')


##cart view ###
def remove_from_cart(request, ticket_id):
    if request.user.is_authenticated:
        current_user = request.user
        # query the cart
        cart = ShoppingCart.objects.get(user=current_user)
        ticket = Ticket.objects.get(id=ticket_id)
        cart.ticket.remove(ticket)
        cart.save()
        return redirect('cart')
    else:
        messages.add_message(request, messages.error, "failed to remove ticket from cart")
        print("Error: failed to remove ticket from cart")
        return redirect('index')


def cart(request):
    if request.user.is_authenticated:
        current_user = request.user

        # query the cart
        cart = ShoppingCart.objects.get(user=current_user)
        # FIXME: if front-end just want tickets in the cart, do:
        tickets = cart.ticket.all()

        amount = sum(ticket_value[ticket.type] for ticket in tickets)

        context = {
            "cart": cart,
            "tickets": tickets,
            "amount": amount
        }
        return render(request, 'payment/cart.html', context)
        # add ticket to context
    else:
        return redirect('index')


def book_ticket(user, card):
    """
    Creates a booking for the user with the card. It marks the seat
    as reserved and removes the shopping cart object. 
    """
    cart = ShoppingCart.objects.get(user=user)

    tickets = cart.ticket.all()

    amount = sum(ticket_value[ticket.type] for ticket in tickets)
    order = Order.objects.create(
        user=user,
        card=card.__str__(),
        order_status='Succeed',
        amount=amount

    )
    for ticket in tickets:
        order.tickets.add(ticket)
        ticket.seat.status = 'X'  # Marking seat as booked
        ticket.seat.save()
        ticket.save()
        # generate tickets
        generate_ticket(ticket_info(ticket))
    cart.delete()


def checkout(request):
    """
    this view is rendering "checkout" page with forms
    """
    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid:
            card = form.save()
            book_ticket(request.user, card)
            return redirect('booking')
    else:
        form = CardForm()
        context = {
            'form': form,
            'buttonText': "Pay",
            'action': "",
            'title': "Checkout"
        }
        return render(request, 'payment/payment.html', context)
