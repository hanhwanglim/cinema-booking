from django.conf import settings
from payment.models import Ticket


# this is the cart for saving tickets' info.
class Cart(object):

    # init&add session to Cart.cart
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_KEY)
        if not cart:
            cart = self.session[settings.CART_SESSION_KEY] = {}
        self.cart = cart

    # TODO:not sure its a good way saving tickets to a session. Might consider sql
    # add a ticket to session and show the ticket price
    def add(self, ticket_id):
        if ticket_id not in self.cart:
            ticket = Ticket.objects.get(ticket_id)
            # apply discount for child or senior
            if ticket.age < 16 or ticket.age >= 65:
                ticket_price = ticket.age * 0.8
            else:
                ticket_price = ticket.age
            self.cart[ticket_id] = {'price': str(ticket_price)}
        else:
            print("Somethings wrong! Shouldn't re-add the same ticket")
        self.save()

    # remove ticket from cart session
    def remove(self, ticket_id):
        if ticket_id in self.cart:
            del self.cart[ticket_id]
        self.save()

    # save session for cart
    def save(self):
        self.session.modified = True

    # list session for cart
    def list(self):
        return self.cart

    # calculate total price in the cart
    def get_total(self):
        return sum(float(ticket['price']) for ticket in self.cart.price())
