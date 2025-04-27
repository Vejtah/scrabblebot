
from functions.movement import Movement
from functions.keys import Keys
from functions.config import Constants
from functions import alg, image as Img

import main_funtions as mf

keys = Keys()
s = alg.Scrabble()

played_moves = []
if Constants.System.running_on_raspberry:
    Mov = Movement()  # movement from Movement

    Mov.release() #  release the motors
    Mov.open()  # open the hand in the start
"""play def"""



"""main loop"""
print("entering main loop...")

print("opening hand...")


#  use try to use finally to release motors
try:
    key = ""           
    while key != keys.AllKeys.KEY_QUIT:

        print(f"press {keys.AllKeys.KEY_PLAY} to play, for help press {keys.AllKeys.KEY_HELP}...")
        key = keys.scan_keys()

        if key == keys.AllKeys.KEY_PLAY:
            print("entering play sequence...")
            rc = mf.play(played_moves)  # play return code
            
            if rc == 0:
                pass
            elif rc == 1:
                
                print("the bot has lost")
                break
                
            elif rc == 2:
                print("not all choose spaces filled: ERROR")
                
                
                
        elif key == keys.AllKeys.KEY_NUMPAD:
            num = keys.numpad()
            print(f"inputted: {num}")

        elif key == keys.AllKeys.KEY_HELP:
            keys.help()

        elif key == keys.AllKeys.KEY_MANUAL:
            print("entering manual movement...")
            if Constants.System.running_on_raspberry:
                Mov.manual()
                Mov.release()

        elif key == keys.AllKeys.KEY_DESTROY_ALL_WINDOWS:
            Img.deinit()

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
    if Constants.System.running_on_raspberry:
        Mov.release()

    Img.deinit()

print("quitting")

