from django.http import HttpResponse
from django.shortcuts import render

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
    return render(request, 'movies/movie.html', context)