from django.http import HttpResponse
from django.shortcuts import render
from payment.forms import SelectDatetimeForm, TestForm
from .models import Movie


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
        form = SelectDatetimeForm(request.POST
                                  ,movie_id=1
                                  )
        if form.is_valid():
            print("SelectDatetimeForm is valid")
            return render("/")
        else:
            print(" Not a valid SelectDatetimeForm")

    else:
        form=SelectDatetimeForm()
    return render(request, 'movies/movie.html', context
                  ,{'form': form}
                  )
