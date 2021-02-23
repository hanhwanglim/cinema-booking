from django import forms
from movies.models import Movie
from halls.models import Showtime


class SelectDatetimeForm(forms.Form):
    #FIXME: Don't know if we must have this part
    class Meta:
        # fields = ('movie_id', 'selected_showtime')
        # movie_id = forms.IntegerField()
        pass

    def __init__(self, *args, **kwargs):
        movie_id=kwargs.pop('movie_id',None )
        super(SelectDatetimeForm, self).__init__(*args, **kwargs)

        #use movie_id to query available_datetime
        if movie_id:
            available_datetime = Showtime.objects.all().filter(movie_id=movie_id)
            self.fields['selected_showtime'] = forms.ChoiceField(
                choices=tuple([(a_time.id, a_time) for a_time in available_datetime]))


class SeatForm(forms.Form):
    def __init__(self, *args, **kwargs):
        showtime_id = kwargs.pop('showtime_id', None)
        super(SelectDatetimeForm, self).__init__(*args, **kwargs)

        #TODO: use showtime to grab all available seats
        if showtime_id:
            # available_seats =
            pass
