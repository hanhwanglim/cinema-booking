from django.db import models
from movies.models import Movie
from users.models import User
from halls.models import Hall, Seat, Showtime


# # Create your models here.

class CardDetails(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    cardNumber: str = models.CharField(max_length=500, null=True)
    first4Digits = models.IntegerField(null=True)
    cardHolderFirstName = models.CharField(max_length=100, null=True)
    cardHolderLastName = models.CharField(max_length=100, null=True)
    ExpireYear = models.IntegerField(null=True, help_text="Please input 2 digits YY")
    ExpireMonth = models.IntegerField(null=True, help_text="Please input 2 digits MM")
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.id)


class Ticket(models.Model):
    # to calculate ticket price use user's age
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    seat = models.ForeignKey(Seat, null=True, on_delete=models.SET_NULL)

    # can query time, hall and movie info from showtime
    showtime = models.ForeignKey(Showtime, null=True, on_delete=models.SET_NULL)

    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.id)


class Order(models.Model):
    STATUS = (
        ('Unpaid', 'Unpaid'),
        ('Pending', 'Pending'),
        ('Succeed', 'Succeed'),
    )

    # one order for one user and a card
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    Card = models.ForeignKey(CardDetails, null=True, on_delete=models.SET_NULL)

    # one order can have many tickets
    tickets = models.ManyToManyField(Ticket)

    status = models.CharField(max_length=200, null=True, choices=STATUS)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    amount = models.FloatField(null=True)

    def __str__(self):
        return str(self.id)
