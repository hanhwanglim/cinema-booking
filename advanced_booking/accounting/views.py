from django.shortcuts import render
from datetime import date, timedelta
from django.utils import timezone
from movies.models import Movie
from payment.models import Order


def get_weekly_income(date):
    """
    Queries the order table for orders within our given range. 
    (last week to :param date)
    Formats the data into an array
    [
        [date string, amount],
        [date string, amount],
        , ...
    ]
    """
    # NOTE This can definitely implemented in a more efficient way

    last_week = date - timedelta(days=7)
    # Because the query would be today : 00:00:00 it would not get 
    # todays things. 
    midnight = date + timedelta(days=1) - timedelta(microseconds=1)
    order = Order.objects.filter(date_created__range=[last_week, midnight])
    # Creating array of dates from last_week to date
    date_array = []
    for i in range(7):
        date_array.insert(0, f'{(date - timedelta(days=i)).strftime("%Y-%m-%d")}')

    # Adding the sum together
    data = {
        f'{date_array[0]}': 0,
        f'{date_array[1]}': 0,
        f'{date_array[2]}': 0,
        f'{date_array[3]}': 0,
        f'{date_array[4]}': 0,
        f'{date_array[5]}': 0,
        f'{date_array[6]}': 0,
    }

    for o in order:
        data[f'{o.date_created_to_string()}'] += o.amount

    # Formatting data
    data_2 = []
    for i in range(len(date_array)):
        d = date_array[i]
        data_2.append([d, data[d]])
    
    return data_2


def accounting(request):
    """
    Queries the database for the week's income.
    """
    today = timezone.now()
    data = get_weekly_income(today)

    context = {
        'data': data
    }

    return render(request, 'accounting/chart.html', context)


def movie_income(request, movie_id):

    return render(request, 'accounting/chart.html')
