from django.db import models
from movies.models import Movie
from users.models import User
from halls.models import Hall, Seat, Showtime


class CardDetail(models.Model):
    user = models.ManyToManyField(User)
    card_number         = models.CharField(max_length=20)
    card_holder_name    = models.CharField(max_length=100)
    expire_month        = models.IntegerField(null=True)
    expire_year         = models.IntegerField(null=True)

    def __str__(self):
        return f'**** **** **** {self.card_number[-4:]}'


class Ticket(models.Model):
    # ticket holder age, might apply discount when adding to cart
    # age = models.IntegerField(null=True)
    seat = models.ForeignKey(Seat, null=True, on_delete=models.SET_NULL)

    AGE_CHOICES = (
        ("CHILD", "Child(Under 16)"),
        ("ADULT", "Adult(17-64)"),
        ("SENIOR", "Senior(Over 65)"),
    )

    type = models.CharField(
        max_length=100,
        choices=AGE_CHOICES,
        default="ADULT",
    )

    # can query time, hall and movie info from showtime
    showtime = models.ForeignKey(
        Showtime, null=True, on_delete=models.SET_NULL)

    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.id)


class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    ticket = models.ManyToManyField(Ticket)

    def __str__(self):
        return f'{self.user} - {self.ticket}'


class Order(models.Model):
    STATUS = (
        ('Unpaid', 'Unpaid'),
        ('Pending', 'Pending'),
        ('Succeed', 'Succeed'),
    )

    # one order for one user and a card
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    card = models.CharField(max_length=20, null=True)
    # Card = models.ForeignKey(CardDetail, null=True, on_delete=models.SET_NULL)

    # one order can have many tickets
    tickets = models.ManyToManyField(Ticket)

    order_status = models.CharField(max_length=200, null=True, choices=STATUS)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    amount = models.FloatField(null=True)

    def __str__(self):
        return f'{self.id} - {self.order_status}'
