import time

""" split into Classes"""
"""__init__"""

from code.main.functions import shit as sh, alg

from code.main.functions.movement import Movement

Mov = Movement()
s = alg.Scrabble()

from code.main.main_functions import main_funtions as mf

#F = Functions()

Mov.release() #  release the motors

"""
file to test the code in different ways
"""

def mam_ret(x, y):
    Mov.move(x + 0,
             y - 5,
             poss_check=False)


if __name__ == "__main__":
    try:
        #Mov.open()
        #Mov.move(-20, 0, poss_check=False)
        Mov.ret()
        Mov.open()

        mf.grab_letter(0)

        time.sleep(4)
        Mov.release()

    finally:
        pass
