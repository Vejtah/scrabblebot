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

from main_control import Functions

Mov = Movement()  # movement from Movement
Cons = Constants()
Sht = SHIT()
keys = Keys()
Img = Image()
s = Scrabble()

Functions = Functions()

Mov.release() #  release the motors

"""
file to test the code in different ways
"""

if __name__ == "__main__":
    Functions.grab_letter(0)
