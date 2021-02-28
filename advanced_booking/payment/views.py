from django.shortcuts import render, redirect
from .forms import PaymentForm
from django.http import HttpResponse
from movies.models import Movie, Ticket
from halls.models import Showtime
from .models import Ticket, Order



# Create your views here.


def create_new_ticket(request, seat_id, showtime_id):
    '''
    create a unpaid order
    '''
    if seat_id and showtime_id:
        #create a new ticket
        new_ticket = Ticket(age=20, seat_id=seat_id, showtime_id=showtime_id)

        # TODO: add multiple ticket per order support

    else:
        return redirect('index')


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
