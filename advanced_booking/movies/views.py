from django.http import HttpResponse
from django.shortcuts import render
from payment.forms import SelectDatetimeForm
from .models import Movie
from halls.models import Showtime


def index(request):
    movie_list = Movie.objects.all()
    context = {
        'movie_list': movie_list,
    }
    return render(request, 'movies/index.html', context)


def movie(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    context = {
        'movie': movie,
    }

    if request.method == 'POST':
        form = SelectDatetimeForm(request.POST, movie_id=1)

        if form.is_valid():
            print("SelectDatetimeForm is valid")
            selected_showtime = form.cleaned_data['selected_showtime']
            # TODO: PASS showtime info to seat page.
            # selected_showtime_id =
            # return render("/")
        else:
            print(" Not a valid SelectDatetimeForm")
    else:
        # create a Datatime form for the current page movie
        form = SelectDatetimeForm(movie_id=1)
        # add form to conext
        context['form'] = form

    return render(request, 'movies/movie.html', context)


def seat(request, showtime_id):
    pass
