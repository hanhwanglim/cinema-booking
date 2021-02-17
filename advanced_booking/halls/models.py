from django.db import models


class Hall(models.Model):
    # TODO we probably dont want this to be null
    name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f'{self.name}'

 
class Seat(models.Model):
    SEAT_STATUS = [
        ('X', 'Seat Taken'),
        ('O', 'Seat Available'),
        ('*', 'Seat Being Booked')
    ]
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, null=False)
    row_number = models.PositiveSmallIntegerField()
    seat_number = models.PositiveSmallIntegerField()
    vip = models.BooleanField(default=False)
    status = models.CharField(max_length=1, choices=SEAT_STATUS)

    def __str__(self):
        return f'Seat ({self.row_number}, {self.seat_number})'
