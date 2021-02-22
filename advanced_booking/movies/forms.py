from django import forms
from .models import Movie
from halls.models import Showtime


# creating a form
class Select_Datatime_Form(forms.Form):
    class Meta:
    movie_id = forms.IntegerField()
    if movie_id:
        available_date = Showtime.filter(movie.id = movie_id).all().time.date

        picked_date = forms.ModelChoiceField(queryset=available_date)
        if picked_date:
            available_time = Showtime.filter(movie.id = movie_id).all().time.time
            picked_time = forms.ModelChoiceField(queryset=available_time)

    selected_showtime = Showtime.filter(movie.id=movie_id).filter(time = available_date).filter(time =available_date).first()

    return selected_showtime
