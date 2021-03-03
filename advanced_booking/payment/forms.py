# pip install django-credit-cards needed !!!!!!
from django import forms
from movies.models import Movie
from halls.models import Showtime, Seat
from creditcards.forms import CardNumberField, CardExpiryField, SecurityCodeField


class PaymentForm(forms.Form):
    number = CardNumberField(label='Card Number')
    expiryDate = CardExpiryField(label='Expiration Date')
    securityCode = SecurityCodeField(label='CVV/CVC')
    name = forms.CharField(label="Name", error_messages={'required': 'Please enter the name written on your card.'})


class SelectDatetimeForm(forms.Form):
    """
    This form provides a datetime choice field for a ticket
    """

    def __init__(self, *args, **kwargs):
        movie_id = kwargs.pop('movie_id', None)
        super(SelectDatetimeForm, self).__init__(*args, **kwargs)

        # use movie_id to query available_datetime
        if movie_id:
            available_datetime = Showtime.objects.all().filter(movie_id=movie_id)
            self.fields['selected_showtime'] = forms.ChoiceField(
                choices=tuple([(a_time.id, a_time) for a_time in available_datetime]))


class SelectSeatForm(forms.Form):
    """
    This form provides a SEAT choice field and a AGE choice field for a ticket
    """

    def __init__(self, *args, **kwargs):
        showtime_id = kwargs.pop('showtime_id', None)
        super(SelectSeatForm, self).__init__(*args, **kwargs)

        # use showtime to grab all available seats
        if showtime_id:
            available_seats = Seat.objects.all().filter(showtime_id=showtime_id)
            self.fields['selected_seats'] = forms.ChoiceField(
                choices=tuple([(a_seat.id, a_seat) for a_seat in available_seats]))

    # add
    AGE_CHOICES = (
        ("Child", "Child(Under 16)"),
        ("Adult", "Adult(17-64)"),
        ("Senior", "Senior(Over 65)"),
    )

    ticket_type = forms.ChoiceField(choices=AGE_CHOICES)
