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
    Mov.move(x + 0,
             y + 5,
             poss_check=False)


if __name__ == "__main__":
    try:
        #Mov.open()
        #Mov.move(-20, 0, poss_check=False)

        mam_ret(0, 0)

        steps = int(input("steps"))

        Mov.move(0, -steps)
        time.sleep(3)
        mam_ret(0, steps)

        #Mov.ret()

        #Mov.move_to(0, 0)
        Mov.close()
        #Mov.ret()
        time.sleep(4)
        Mov.release()

    finally:
        pass
