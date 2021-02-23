from django import forms
from movies.models import Movie
from halls.models import Showtime



#FIXME: not sure why the view is not showing this form
class SelectDatetimeForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.movie_id = kwargs.pop('movie_id',[])
        super(SelectDatetimeForm, self).__init__(*args, **kwargs)
        if self.movie_id:
            self.fields['movie'].initial = self.movie_id
            available_datetime = Showtime.objects.all().filter(movie_id=self.movie)
            selected_showtime = forms.ChoiceField(choices=[(x.time, x.time) for x in available_datetime])

    class Meta:
        test_field = forms.IntegerField(label="test a number ")
        selected_showtime = forms.ChoiceField()

class TestForm(forms.Form):
    class Meta:
        test_form_field = forms.IntegerField(label="test a number ")

