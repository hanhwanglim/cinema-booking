import os, sys
import time
from PIL import Image, ImageFont, ImageDraw
from .models import Ticket
from datetime import datetime


# generate a printable ticket with
def generate_ticket(ticket_info):
    # TODO: Test if it works without absolute path in win/linux

    # open image for tests
    ticket_tmp = Image.open("payment/resources/templates/ticket_tmp.jpg")
    title_font = ImageFont.truetype("payment/resources/fonts/Powerline.ttf", 50)

    # set text
    # date_font = title_font
    # type_text = type

    # draw
    image_editable = ImageDraw.Draw(ticket_tmp)
    # left hand side
    image_editable.text((100, 275), ticket_info["title"], (0, 0, 0), font=title_font)
    image_editable.text((210, 360), ticket_info["certificate"], (0, 0, 0), font=title_font)

    image_editable.text((205, 440), ticket_info["date"], (0, 0, 0), font=title_font)
    image_editable.text((205, 490), ticket_info["time"], (0, 0, 0), font=title_font)
    image_editable.text((250, 540), ticket_info["screen"], (0, 0, 0), font=title_font)

    # right hand side
    image_editable.text((750, 170), ticket_info["ticket_type"], (0, 0, 0), font=title_font)
    image_editable.text((1000, 665), "Row " + ticket_info["seat_row"], (0, 0, 0), font=title_font)
    image_editable.text((1000, 715), "No. " + ticket_info["seat_number"], (0, 0, 0), font=title_font)

    # for debugging
    # ticket_tmp.show()

    ticket_id = ticket_info["ticket_id"]
    try:
        ticket_tmp.save(f"payment/resources/rendered_tickets/ticket{ticket_id}.pdf")
    except:
        os.remove(f"resources/rendered_tickets/ticket{ticket_id}.pdf")
        ticket_tmp.save(f"resources/rendered_tickets/ticket{ticket_id}.pdf")


def ticket_info(ticket):
    movie_title = ticket.showtime.movie.title
    certificate = ticket.showtime.movie.certificate
    movie_date = ticket.showtime.time.date().strftime("%m/%d/%Y")
    movie_time = ticket.showtime.time.time().strftime("%H:%M")
    screen = ticket.showtime.hall.name
    ticket_type = ticket.type

    row_number = str(ticket.seat.row_number)
    seat_number = str(ticket.seat.seat_number)

    ticket_id = str(ticket.id)

    return {"title": movie_title,
            "certificate": certificate,
            "date": movie_date,
            "time": movie_time,
            "screen": screen,
            "ticket_type": ticket_type,
            "seat_row": row_number,
            "seat_number": seat_number,
            "ticket_id": ticket_id
            }

# if __name__ == "__main__":
#     # movie_title,rating,movie_date,screen, type,seat, movie_id
#     generate_ticket("TEST MOVIE TITLE", "R18", str(datetime.now()), "hall 2", "ADULT", "A1", 1)
