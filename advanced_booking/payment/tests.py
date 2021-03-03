from datetime import date, datetime, timezone
from django.urls import reverse
from django.test import TestCase, SimpleTestCase
from movies.models import Movie
from halls.models import Showtime, Hall
from .models import ShoppingCart, Ticket
from users.models import User

from users.tests import create_user
from movies.tests import create_hall, create_movie, create_showtime

from .views import create_new_ticket, add_to_cart,remove_from_cart




class MovieViewTests(TestCase):
    def test_create_ticket(self):
        show = create_showtime(
            create_hall(),
            create_movie(f'Title of Movie 1'),
            datetime(2021, 1, 1, 12, 0, 0, 0, timezone.utc)
        )
        # created ticket has default type :adult
        ticket = Ticket.objects.create(seat_id=1, showtime=show)
        test_ticket = create_new_ticket(1, show.id, "Adult")

        self.assertEqual(ticket.showtime, test_ticket.showtime)
        self.assertEqual(ticket.seat_id, test_ticket.seat_id)
        self.assertEqual(ticket.type, test_ticket.type)

    def test_add_to_cart(self):
        show = create_showtime(
            create_hall(),
            create_movie(f'Title of Movie 1'),
            datetime(2021, 1, 1, 12, 0, 0, 0, timezone.utc)
        )

        create_user('123@test.com', 'test_user1', 'qwe@123')
        result = add_to_cart(1, show.id, "Adult", user=User.objects.get(id=1))
        #test adding function
        self.assertEqual(result, True)
        #test query back
        cart = ShoppingCart.objects.get(user=User.objects.get(id=1))
        self.assertNotEqual(cart,None)
        self.assertEqual(cart.ticket.first().id,1)


    def test_remove_ticket(self):
        show = create_showtime(
            create_hall(),
            create_movie(f'Title of Movie 1'),
            datetime(2021, 1, 1, 12, 0, 0, 0, timezone.utc)
        )

        create_user('123@test.com', 'test_user1', 'qwe@123')
        result = add_to_cart(1, show.id, "Adult", user=User.objects.get(id=1))
        cart = ShoppingCart.objects.get(user=User.objects.get(id=1))
        self.assertEqual(cart.ticket.first().id,1)
        test_return = remove_from_cart(user=User.objects.get(id=1),ticket_id=1)
        self.assertEqual( test_return,True)
        self.assertEqual(cart.ticket.all().first(),None)
        #test if it's removed

