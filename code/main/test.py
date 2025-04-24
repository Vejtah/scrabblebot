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

def mam_ret(x, y):
    Mov.move(-x + 5, -y, poss_check=False)


if __name__ == "__main__":
    try:
        #Mov.open()
        steps = int(input("steps"))

        Mov.move(-steps, 0)
        time.sleep(3)
        mam_ret(-steps, 0)

        #Mov.ret()

        #Mov.move_to(0, 0)
        Mov.close()
        #Mov.ret()

    finally:
        time.sleep(4)
        Mov.release()
