from django.contrib import admin

from .models import Ticket, CardDetails, Order
from movies.models import Movie
from halls.models import Hall, Seat, Showtime


# Register your models here.
class TicketInterface(admin.ModelAdmin):
    list_display = ('__str__', 'showtime', 'seat', 'age')
    search_fields = ['age', 'seat', 'showtime']
    readonly_fields = ()
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class CardDetailsInterface(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'first4Digits', 'cardHolderLastName')
    search_fields = ['user', 'cardHolderLastName', 'cardHolderFirstName']
    readonly_fields = ()
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class OrderInterface(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'Card', 'get_tickets', 'status', 'amount')
    search_fields = ['user', 'tickets']
    readonly_fields = ()
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    
    # print all tickets in list_display
    def get_tickets(self, obj):
        return ", ".join([str(p) for p in obj.tickets.all()])


admin.site.register(Ticket, TicketInterface)
admin.site.register(CardDetails, CardDetailsInterface)
admin.site.register(Order, OrderInterface)
