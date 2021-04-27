from halls.models import Showtime
from django.shortcuts import redirect, render
from datetime import date, timedelta, datetime
from django.utils import timezone
from movies.models import Movie
from payment.models import Order, Ticket


def get_income_between(start_date, end_date):
    """
    Queries the order table for orders within our given range. 
    (:param start_date to :param end_date)
    Formats the data into an array
    [
        [date string, amount],
        [date string, amount],
        , ...
    ]
    """
    # Because the query would be today : 00:00:00 it would not get
    # todays things.
    end_date = end_date + timedelta(days=1) - timedelta(microseconds=1)
    order = Order.objects.filter(date_created__range=[start_date, end_date])

    dates = []
    amount = []

    # Creating array of dates from start date to end date
    for o in order:
        try:
            index = dates.index(o.date_created.date())
            amount[index] += o.amount
        except:
            dates.append(o.date_created.date())
            amount.append(o.amount)

    # Formatting the data for JavaScript parsing
    data_format = []
    for i in range(len(dates)):
        data_format.append(
            [f'new Date({dates[i].year},{dates[i].month - 1},{dates[i].day})', amount[i]])

    return data_format


def accounting(request):
    """
    Queries the database for the week's income.
    """
    try:
        if not request.user.is_admin:
            return redirect('index')
    except:
        return redirect('index')

    all_orders = Order.objects.all()
    overall_income = 0
    for o in all_orders:
        overall_income += o.amount

    if request.method == 'POST':
        start_date = datetime.strptime(request.POST['start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(request.POST['end_date'], '%Y-%m-%d')

        data = get_income_between(start_date, end_date)
        context = {
            'start_date': start_date.strftime("%d-%m-%Y"),
            'end_date': end_date.strftime("%d-%m-%Y"),
            'format_start_date': f'new Date({start_date.year},{start_date.month -1},{start_date.day - 1})',
            'format_end_date': f'new Date({end_date.year},{end_date.month -1},{end_date.day + 1})',
            'data': data,
            'len': range(len(data)),
            'overall_income': overall_income,
        }
        return render(request, 'accounting/chart.html', context)

    today = timezone.now()
    last_week = today - timedelta(days=7)
    data = get_income_between(last_week, today)

    context = {
        'start_date': last_week.strftime("%d-%m-%Y"),
        'end_date': today.strftime("%d-%m-%Y"),
        'format_start_date': f'new Date({last_week.year},{last_week.month -1},{last_week.day - 1})',
        'format_end_date': f'new Date({today.year},{today.month -1},{today.day + 1})',
        'data': data,
        'len': range(len(data)),
        'overall_income': overall_income,
    }

    return render(request, 'accounting/chart.html', context)


def movie_income(request, movie_id):
    try:
        if not request.user.is_admin:
            return redirect('index')
    except:
        return redirect('index')

    movie = Movie.objects.get(pk=movie_id)
    movie_showtime = Showtime.objects.filter(movie=movie)
    tickets = []
    for ms in movie_showtime:
        tickets.append(Ticket.objects.filter(showtime=ms.pk))
    n_child = 0
    n_adult = 0
    n_senior = 0
    revenue = 0
    for i in range(len(tickets)):
        for t in tickets[i]:
            revenue += t.price
            if t.type == "CHILD":
                n_child += 1
            elif t.type == "ADULT":
                n_adult += 1
            elif t.type == "SENIOR":
                n_senior += 1

    context = {
        'n_child': n_child,
        'n_adult': n_adult,
        'n_senior': n_senior,
        'revenue': revenue,
        'movie': movie
    }
    return render(request, 'accounting/movie_chart.html', context)


def create_comparison(start_date, end_date):
    end_date = end_date + timedelta(days=1) - timedelta(microseconds=1)
    tickets = Ticket.objects.filter(date_created__range=[start_date, end_date])
    dates = []
    movies = []

    for t in tickets:
        if t.showtime.movie not in movies:
            movies.append(t.showtime.movie)
        if t.date_created.date() not in dates:
            dates.append(t.date_created.date())

    data = [[d] for d in dates]

    for d in data:
        for i in range(len(movies)):
            d.append(0)

    for t in tickets:
        date_index = dates.index(t.date_created.date())
        movie_index = movies.index(t.showtime.movie)
        data[date_index][movie_index + 1] += t.price

    # Format data
    for i in range(len(data)):
        data[i][0] = f'new Date({data[i][0].year},{data[i][0].month -1},{data[i][0].day})'
    print(data)

    return data, movies


def compare(request):
    try:
        if not request.user.is_admin:
            return redirect('index')
    except:
        return redirect('index')

    if request.method == 'POST':
        start_date = datetime.strptime(request.POST['start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(request.POST['end_date'], '%Y-%m-%d')

        data = create_comparison(start_date, end_date)
        # print(data)
        context = {
            'start_date': start_date.strftime("%d-%m-%Y"),
            'end_date': end_date.strftime("%d-%m-%Y"),
            'data': data[0],
            'movie': data[1],
            'format_start_date': f'new Date({start_date.year},{start_date.month -1},{start_date.day - 1})',
            'format_end_date': f'new Date({end_date.year},{end_date.month -1},{end_date.day + 1})'
        }
        return render(request, 'accounting/compare.html', context)
    else:
        start_date = date.today() - timedelta(days=7)
        end_date = date.today()

        data = create_comparison(start_date, end_date)
        # print(data[1])
        context = {
            'start_date': start_date.strftime("%d-%m-%Y"),
            'end_date': end_date.strftime("%d-%m-%Y"),
            'data': data[0],
            'movie': data[1],
            'format_start_date': f'new Date({start_date.year},{start_date.month -1},{start_date.day - 1})',
            'format_end_date': f'new Date({end_date.year},{end_date.month -1},{end_date.day + 1})'

        }
        return render(request, 'accounting/compare.html', context)
