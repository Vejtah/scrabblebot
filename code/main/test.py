import time
#from wsgiref.util import request_uri

from tqdm import tqdm

""" split into Classes"""
"""__init__"""

from movement import Movement
from constans import Constants
from shit import SHIT
from keys import Keys
from image import Image
from alg import Scrabble

#from main_control import Functions

Mov = Movement()  # movement from Movement
Cons = Constants()
Sht = SHIT()
keys = Keys()
Img = Image()
s = Scrabble()

#F = Functions()

Mov.release() #  release the motors

"""
file to test the code in different ways
"""

def move_to(target_x: int, target_y: int)->None:
    print(Mov.move_to(target_x, target_y))
    x_move_by, y_move_by = Mov.move_to(target_x, target_y)

    Mov.move(x_move_by, y_move_by)

def move_to_piece(x, y):

    x_target, y_target = Mov.move_to_piece(x, y)


    move_to(x_target, y_target)

def ret() -> None:
    move_to_piece(14, 10)
    time.sleep(Mov.sleep)
    move_to(0, 0)
    Mov.move(-5, -5)
    Cons.s_x, Cons.s_y = 0, 0 # reset the x and y var
    #Mov.open() # open the hand


def grab_letter(letter_pos) -> None:
    move_to_piece(14, 10)
    time.sleep(0.5)
    letter_x_pos = letter_pos * 2  # gaps between holders

    move_to_piece(0, 10)
    time.sleep(0.5)

    move_to_piece(letter_x_pos, 11)  # slide on to the tile

    Mov.close()
    time.sleep(0.5)

    move_to_piece(letter_x_pos, 10)  # move out




if __name__ == "__main__":
    try:
        Mov.open()
        Mov.move(-50, -50)
    finally:
        Mov.release()
