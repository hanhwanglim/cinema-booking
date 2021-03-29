from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from payment.forms import SelectDatetimeForm, SelectSeatForm
from .models import Movie
from halls.models import Showtime, Seat
from payment.views import add_to_cart
from payment.models import Order, ShoppingCart
import operator


def index(request):
    messages.get_messages(request)
    movie_list = Movie.objects.all()
    context = {
        'movie_list': movie_list,
    }
    return render(request, 'movies/index.html', context)


def movie(request, movie_id):
    try:
        movie = Movie.objects.get(pk=movie_id)
    except:
        return index(request)

    context = {
        'movie': movie,
    }

    if request.method == 'POST':
        form = SelectDatetimeForm(request.POST, movie_id=movie_id)

        if form.is_valid():
            print("SelectDatetimeForm is valid")
            selected_showtime_id = form.cleaned_data['selected_showtime']
            if request.user.is_authenticated:
                return redirect('seat', selected_showtime_id)
            else:
                return redirect('login')
        else:
            print(" Not a valid SelectDatetimeForm")
    else:
        # create a Datatime form for the current page movie
        form = SelectDatetimeForm(movie_id=movie_id)
        # add form to conext
        context['form'] = form

    return render(request, 'movies/movie.html', context)


def seat(request, showtime_id):
    """
    view function for the seat choosing page
    """
    messages.get_messages(request)
    context = {

    }
    if showtime_id:
        showtime = Showtime.objects.get(pk=showtime_id)
        movie = showtime.movie
        hall = showtime.hall
        seats = Seat.objects.all().filter(showtime_id=showtime_id)

        # TODO: add required info for front-end
        context['movie'] = movie
        context['hall'] = hall
        if request.method == 'POST':
            form = SelectSeatForm(request.POST, showtime_id=showtime_id)

            if form.is_valid():
                name = request.POST.get('seats')
                print(name)
                print("SelectSeatForm is valid")
                selected_seat_id = form.cleaned_data['selected_seats']
                print(selected_seat_id)
                ticket_type = form.cleaned_data['ticket_type']
                # add cart for login user
                if request.user.is_authenticated:
                    current_user = request.user
                    # create ticket and add to cart
                    print("successfully created a ticket and added to cart")
                    messages.success(request, "successfully added your chosen ticket to the cart.")
                    add_to_cart(request, name, showtime_id, ticket_type)
                    # return redirect(add_to_cart, seat_id=name, showtime_id=showtime_id,
                    #                 ticket_type=ticket_type)
                    return redirect('seat', showtime_id=showtime_id)
                else:
                    print("Error: form not valid!")
                    return redirect('index')
            else:
                print(" Not a valid SelectDatetimeForm")
        else:
            # create a Datatime form for the current page movie
            form = SelectSeatForm(showtime_id=showtime_id)
            # add form to conext
            seats = Seat.objects.all().filter(showtime_id=showtime_id)

            current_user = request.user

            try:
                cart = ShoppingCart.objects.get(user=request.user)
            except:
                cart = ShoppingCart.objects.create(user=request.user)
                cart = ShoppingCart.objects.get(user=current_user)
                cart.save()

            tickets = cart.ticket.all()

            view_tickets = []

            flag = 0
            for x in seats:
                for y in tickets:
                    if (y.seat.id == x.id):
                        print(str(y.seat.id) + " " + str(x.id))
                        flag = 1
                        y.seat.status = '*'
                        view_tickets.append(y.seat)

                if (flag == 0):
                    view_tickets.append(x)

                else:
                    flag = 0
            for same in view_tickets:
                for y in tickets:
                    if (y.seat.id == same.id and same.status == 'O'):
                        view_tickets.remove(same)
            context['form'] = form
            context['seatlist'] = view_tickets
            context['tickets'] = tickets

    return render(request, 'movies/seat.html', context)


def search(request):
    # search functionality
    srch = request.GET['query']  # search value
    sort = request.GET['sort']  # sort value
    search_for = request.GET['search_for']  # "search by" value
    # next 6 lines for "sort by" functionality
    if search_for == 'title':
        movies = Movie.objects.filter(title__icontains=srch)
    if search_for == 'director':
        movies = Movie.objects.filter(director__icontains=srch)
    if search_for == 'lead_actor':
        movies = Movie.objects.filter(lead_actor__icontains=srch)
    # default sort
    movies = sorted(movies, key=operator.attrgetter('title'))
    # next 16 lines for sort functionality
    if sort == 'A-Z':
        movies = sorted(movies, key=operator.attrgetter('title'))
    if sort == 'Z-A':
        movies = sorted(movies, key=operator.attrgetter('title'), reverse=True)
    if sort == 'year(1-9)':
        movies = sorted(movies, key=operator.attrgetter('premier_date'))
    if sort == 'year(9-1)':
        movies = sorted(movies, key=operator.attrgetter('premier_date'), reverse=True)
    if sort == 'duration(1-9)':
        movies = sorted(movies, key=operator.attrgetter('duration'))
    if sort == 'duration(9-1)':
        movies = sorted(movies, key=operator.attrgetter('duration'), reverse=True)
    if sort == 'rating(1-9)':
        movies = sorted(movies, key=operator.attrgetter('rating'))
    if sort == 'rating(9-1)':
        movies = sorted(movies, key=operator.attrgetter('rating'), reverse=True)
    # final parameters for form
    params = {'movies': movies,
              'search': srch}
    return render(request, 'movies/search_result.html', params)


# temp view for the search bar.
# !!!!!Must be deleted after transfer !!!!!!!
def searchbar(request):
    return render(request, 'movies/search.html')
