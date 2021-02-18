"""
How to use:
    In the directory of manage.py
    $ python manage.py shell < halls/create_seats.py
    
    hall and seats should be created automatically and assigned.
"""

from halls.models import Seat, Hall


# Create hall
h = Hall(name=f'Hall 1')
h.save()

# Create seats
ROW = 5
SEAT_NUM = 12
for i in range(1, ROW + 1):
    for j in range(1, SEAT_NUM + 1):
        s = Seat(
            row_number = i,
            seat_number = j,
            status = 'X',
            vip = i % 5 == 3,
            hall = h,
        )
        s.save()
