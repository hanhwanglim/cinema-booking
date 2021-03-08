
import os, sys
import time
from PIL import Image, ImageFont, ImageDraw 


#generate a printable ticket with 
def generate_ticket(title,rating,date,screen, type,seat, movie_id):
    

    #TODO: Test if it works without absolute path in win/linux
    # script_dir = os.path.dirname(__file__) 
    # abs_file_path = os.path.join(script_dir, "ticket_tmp.jpg")
    # ticket_tmp = Image.open(abs_file_path)

    #open iamge
    ticket_tmp = Image.open("resources/templates/ticket_tmp.jpg")
    
    #set text
    title_font = ImageFont.truetype("resources/fonts/Powerline.ttf",50)
    

    date_font = title_font

    
    type_text = type
    #draw
    image_editable = ImageDraw.Draw(ticket_tmp)
    #left hand side
    image_editable.text((100,275), title, (0, 0, 0), font=title_font)
    image_editable.text((210,360), rating, (0, 0, 0), font=title_font)

    image_editable.text((205,440), date, (0, 0, 0), font=title_font)
    image_editable.text((205,490), date, (0, 0, 0), font=title_font) #put as date for now
    image_editable.text((250,540), screen, (0, 0, 0), font=title_font)
    
    #right hand side
    image_editable.text((750,170), type, (0, 0, 0), font=title_font)
    image_editable.text((1000,665), seat, (0, 0, 0), font=title_font)
    
    # for debugging
    ticket_tmp.show()

    # try:
    #     ticket_tmp.save(f"resources/rendered_tickets/ticket{movie_id}.pdf")
    # except:
    #     os.remove(f"resources/rendered_tickets/ticket{movie_id}.pdf")
    #     ticket_tmp.save(f"resources/rendered_tickets/ticket{movie_id}.pdf")

def ticket_info(ticket):
    movie_title = ticket.showtime.movie.title
    
from datetime import datetime
if __name__ == "__main__":
    # movie_title,rating,movie_date,screen, type,seat, movie_id
    generate_ticket("TEST MOVIE TITLE","R18",str(datetime.now()),"hall 2","ADULT","A1", 1)

