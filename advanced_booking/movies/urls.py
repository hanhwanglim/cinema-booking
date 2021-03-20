from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('movie/<int:movie_id>/', views.movie, name='movie'),
    path('movie/choose_your_seat/<int:showtime_id>/', views.seat, name='seat'),
    path('search',views.searchbar,name='tempsearchpage'), #temp path to search bar. Must be deleted after
    path('search_results',views.search,name='search_results') #temp path to search results. Must be updated/deleted
]
