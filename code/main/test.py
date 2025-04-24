import time
#from wsgiref.util import request_uri

from tqdm import tqdm

""" split into Classes"""
"""__init__"""

import shit as sh
import data as d
import image as img

import alg
from movement import Movement
from constants import Constants
Mov = Movement()
s = alg.Scrabble()

#F = Functions()

Mov.release() #  release the motors

"""
file to test the code in different ways
"""


if __name__ == "__main__":
    try:
        Mov.open()
        Mov.move_to(220, 180)
    
    finally:
        Mov.release()
