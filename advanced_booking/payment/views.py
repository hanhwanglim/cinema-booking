from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.core.mail import send_mail, EmailMessage
from .forms import CardForm, PayByCashForm
from movies.models import Movie
from halls.models import Showtime
from .forms import QuickCheckoutForm
from .models import Ticket, Order, ShoppingCart, CardDetail
from .create_ticket_image import ticket_info, generate_ticket
import os
import payment
# adjust discount for each type here.
from advanced_booking import settings


def create_new_ticket(seat_id, showtime_id, ticket_type):
    """
    create a ticket
    """
    if seat_id and showtime_id and ticket_type:
        # create a new ticket
        # print("ticket_type is:")
        # print(ticket_type)
        new_ticket = Ticket.objects.create(
            seat_id=seat_id, showtime_id=showtime_id, type=ticket_type)
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
                if Showtime.objects.get(id=showtime_id).movie.certificate in ["18", "R18"]:
                    messages.error(request, "Movie certificate Limitation:"
                                            " can't buy for child")
                    print("Error:Movie Rating Limitation")
                    # return redirect('index')
                    return False
            new_ticket = create_new_ticket(seat_id, showtime_id, ticket_type)
            try:
                cart = ShoppingCart.objects.get(user=request.user)
                cart.ticket.add(new_ticket)
            except:
                cart = ShoppingCart.objects.create(user=request.user)
                cart.ticket.add(new_ticket)
                cart.save()
            # return redirect('cart')
            return True
        else:
            messages.error(request, "Can't create ticket"
                                    " due to null values")
            print("Error: Can't create ticket due to null values")
            # return redirect('index')
            return False
    else:
        messages.error(request, "Unauthenticated user!")
        print("Error: Unauthenticated user!")
        # return redirect('index')
        return False


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
        messages.error(request, "failed to remove ticket from cart")
        print("Error: failed to remove ticket from cart")
        return redirect('index')


def cart(request):
    # handle some messages from failed booking
    messages.get_messages(request)
    if request.user.is_authenticated:
        current_user = request.user

        # query the cart
        try:
            cart = ShoppingCart.objects.get(user=current_user)
        except:
            cart = ShoppingCart.objects.create(user=request.user)
            cart = ShoppingCart.objects.get(user=current_user)

        # FIXME: if front-end just want tickets in the cart, do:
        tickets = cart.ticket.all()

        amount = sum(ticket.price for ticket in tickets)

        # based on users' saved card info to choose whether show the quick checkout
        if CardDetail.objects.filter(user=current_user).all():

            form = QuickCheckoutForm(request.POST, use_required_attribute=False, user=current_user.id, )
            if request.method == 'POST':
                if form.is_valid():
                    print("QuickCheckoutForm is valid")
                    card = form.cleaned_data['card']
                    if request.user.is_authenticated:
                        if book_ticket(current_user, card):
                            messages.success(
                                request, 'Successfully booked tickets. Check email for your tickets. ')
                            return redirect('booking')
                        else:
                            messages.error(
                                request, "Booking Failed: Some tickets aren't available anymore... Please try again ")
                            return redirect('cart')
                    else:
                        return redirect('login')
                else:
                    print(" Not a valid QuickCheckoutForm")
            else:
                context = {
                    "cart": cart,
                    "tickets": tickets,
                    "amount": amount,
                    "form": form
                }

        else:
            context = {
                "cart": cart,
                "tickets": tickets,
                "amount": amount
            }
        return render(request, 'payment/cart.html', context)
        # add ticket to context
    else:
        # messages.error("Need login!")
        return redirect('login')


def book_ticket(user, card):
    """
    Creates a booking for the user with the card. It marks the seat
    as reserved and removes the shopping cart object.

    Return True if booked successful, else return False
    """
    cart = ShoppingCart.objects.get(user=user)

    tickets = cart.ticket.all()

    trigger = 0  # initial trigger
    for ticket in tickets:
        if ticket.seat.status == 'X':  # any ticket has been booked
            cart.ticket.remove(ticket)
            trigger = 1  # any removed ticket triggered failed to book

    if trigger:
        return False

    amount = sum(ticket.price for ticket in tickets)
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
        generate_ticket(ticket_info(ticket, user))

    cart.delete()
    sendticket(order)

    return True


def sendticket(order):
    """
    Send ticket to user
    """

    print("Trying to send tickets for order" + str(order.id))
    print("Trying to send to:" + str(order.user))
    subject = "Your order" + str(order.id) + "(Digital ticketed included)"
    mail = EmailMessage(subject,
                        'Thank you for booking with us.',
                        settings.EMAIL_HOST_USER,
                        [order.user])
    # path = os.path.dirname(payment.__file__)
    try:
        for ticket in order.tickets.all():
            print("Trying to attach" + f"ticket{ticket.id}.pdf")
            mail.attach_file(
                f"payment/static/rendered_tickets/ticket{ticket.id}.pdf")
        mail.send()
        print("Success: Sent tickets to user's email.")
        return True
    except:
        # big or corrupt
        print("Error: Failed to send email: CAN NOT attach files")
        return False


def book_ticket_staff(user, amount_payed):
    """
    Creates a booking payment by cash for an employee. It marks the seat
    as reserved and removes the shopping cart object.

    Return price if booked successful.
    If user is not authorised(not staff or above) return -1
    If booking of a seat fails return -2
    If amount payed is less than total amount return -3
    """
    if user.is_staff or user.is_admin or user.is_superuser:
        cart = ShoppingCart.objects.get(user=user)
        tickets = cart.ticket.all()

        flag = 0  # initial flag
        for ticket in tickets:
            if ticket.seat.status == 'X':  # if any ticket has been already booked
                cart.ticket.remove(ticket)
                flag = 1  # any removed ticket failed flag it

        if flag:
            return -2
        amount = sum(ticket.price for ticket in tickets)
        if amount_payed < amount:
            return -3
        order = Order.objects.create(
            user=user,
            order_status='Succeed',
            amount=amount
        )

        for ticket in tickets:
            order.tickets.add(ticket)
            ticket.seat.status = 'X'  # Marking seat as booked
            ticket.seat.save()
            ticket.save()
            generate_ticket(ticket_info(ticket, user))  # generate tickets

        cart.delete()
        sendticket(order)
        change = amount_payed - amount
        return change
    else:
        return -1


def get_basket_price(user):
    # returns the total price of the basket
    cart = ShoppingCart.objects.get(user=user)
    tickets = cart.ticket.all()
    return sum(ticket.price for ticket in tickets)


def checkout(request):
    """
    this view is rendering "checkout" page with forms
    """
    if request.method == 'POST':
        form = CardForm(request.POST)

        if form.is_valid():
            print("valid form")
            card = form.save()
            try:
                card.user.add(request.user)
            except:
                pass
            print(card)
            if not book_ticket(request.user, card):
                messages.error(
                    request, 'Some tickets are unavailable. Please try again.')
                return redirect('cart')

            messages.success(
                request, 'Successfully booked tickets. Check email for your tickets. ')
            return redirect('booking')
        else:
            print("invalid checkout form")
            messages.error(request, "Please retry some valid month / year!")
            return redirect('checkout')

    else:
        # check if the user is verified by email (mailtrap)
        if request.user.verified:
            form = CardForm()
            context = {
                'form': form,
                'buttonText': "Pay",
                'action': "",
                'title': "Checkout"
            }
            return render(request, 'payment/payment.html', context)
        else:
            messages.error(
                request, 'Please verify your account by clicking the link in the email.')
            return redirect('cart')


def pay_by_cash(request):
    user = request.user
    messages.get_messages(request)
    if user.is_staff or user.is_admin or user.is_superuser:
        total_price = get_basket_price(user=user)
        if request.method == 'POST':
            form = PayByCashForm(request.POST)
            context = {
                'action': '',
                'amount': total_price,
                'title': "Pay by cash",
                'buttonText': 'Confirm Payment',
                'form': form
            }
            return render(request, 'payment/pay_by_cash.html', context)
        else:
            form = PayByCashForm(request.GET)
            context = {
                'action': '',
                'amount': total_price,
                'title': "Pay by cash",
                'buttonText': 'Confirm Payment',
                'form': form
            }
            if form.is_valid():
                change = book_ticket_staff(user=user, amount_payed=form.cleaned_data['amount_payed'])
                if change > 0:
                    messages.info(request, 'The payment has been accepted')
                    messages.info(request, 'The change is' + str(change))
                    return redirect('index')
                elif change == 0:
                    messages.info(request, 'The payment has been accepted')
                    return redirect('index')
                elif change == -3:
                    messages.error(request, 'The amount payed is less than the total ticket price!')
                elif change == -2:
                    messages.error(request, 'Booking a seat has failed.Check if all requested seats are free!')
                    return redirect('cart')
                elif change == -1:
                    messages.error(request, 'The user is not authorised!')
                    return redirect('index')
            return render(request, 'payment/pay_by_cash.html', context)
    else:
        messages.error(request, 'The user is not authorised!')
        return redirect('index')
