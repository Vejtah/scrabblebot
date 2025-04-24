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

import main_funtions
#F = Functions()

Mov.release() #  release the motors

"""
file to test the code in different ways
"""


if __name__ == "__main__":
    try:
        #Mov.open()
        Mov.ret()

        Mov.move_to(0, 0)
        Mov.close()
        Mov.ret()

    finally:
        time.sleep(4)
        Mov.release()
