
""" split into Classes"""

from movement import Movement
from constans import Constants
from shit import SHIT
from keys import Keys
from image import Image
from alg import Scrabble

from main_functions import Functions

"""__init__"""

Mov = Movement()  # movement from Movement
Cons = Constants()
Sht = SHIT()
keys = Keys()
Img = Image()
s = Scrabble()

Fn = Functions()

Mov.release() #  release the motors

"""play def"""


def play():
    grid, choose = Fn.get_grid()
    Img.show_grid(grid, choose)
    
    word = Fn.best_word(grid, choose)
    if word == 0:
        return 0
    
    Cons.played_moves.append(word[0])  # add word to played moves
    Fn.build_word(word, choose)
    return 1
    

"""main loop"""
print("entering main loop...")

print("opening hand...")

Mov.open() # open the hand in the start
Img.init()

#  use try to use finally to release motors
try:
    key = ""           
    while key != keys.AllKeys.KEY_QUIT:

        print(f"press keys to continue, for help press {keys.AllKeys.KEY_HELP}...")
        key = keys.scan_keys()

        if key == keys.AllKeys.KEY_PLAY:
            print("entering play sequence...")
            if play() == 0:
                print("the bot has lost")
                break
        elif key == keys.AllKeys.KEY_NUMPAD:
            num = keys.numpad()
            print(f"inputted: {num}")

        elif key == keys.AllKeys.KEY_HELP:
            keys.help()

        elif key == keys.AllKeys.KEY_MANUAL:
            print("entering manual movement...")
            Mov.manual()
            Mov.release()


        elif key == keys.AllKeys.KEY_QUIT: # confirm to quit 
            print(f"confirm to quit ({keys.AllKeys.KEY_CONFIRM})")
            key = keys.scan_keys()
            if key == keys.AllKeys.KEY_CONFIRM:
                print("confirmed")
                key = keys.AllKeys.KEY_QUIT # confirmed quit (set back to confirmed...)
        else:
            print(key)


#except Exception as e:
    #print(e)
    
finally:
    """end sequence"""
    Mov.release()
    Img.end()

print("quitting")

