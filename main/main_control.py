import time
from tqdm import tqdm

""" split into Classes"""
"""__init__"""

from movement import Movement
from constans import Constants
from shit import SHIT
from keys import Keys
from image import Image

Mov = Movement()  # movement from Movement
Cons = Constants()
shit = SHIT()
keys = Keys()
Img = Image()

"""play def"""



def GetGrid():
    print("transforing frame...")
    transformedFrame = Img.GetTransformedFrame()

    print("spliting frame...")
    frames = Img.split_into_grid(transformedFrame, Cons.rows, Cons.cols)

    print("selecting frames...")
    frames = Img.selectFrames(frames)

    # preform a check 
    if len(frames) == 157:
        print("Frame Selection : OK")
    else:
        print("Error in split or select: ERROR")
        return # add a returnpoint IDK

    print("transforming frames to string...")
    letters = []

    for frame in tqdm(frames, desc="img to str"):  # use tqdm to crate a loading bar
        letters.append(shit.SHIT(frame))
        time.sleep(0.005)  # remove (simulate the loading)
    
    print("transforming into a dict")
    
    choose, grid = Img.transformList(letters)
    return grid, choose


def play():
    grid, choose = GetGrid()
    Img.show_grid(grid, choose)
    

"""main loop"""
print("entering main loop...")

print("opening hand...")

Mov.open() # open the hand in the start


key = ""           
while key != keys.AllKeys.KEY_QUIT:

    print(f"press keys to continue, for help press {keys.AllKeys.KEY_HELP}...")
    key = keys.scanKeys()

    if key == keys.AllKeys.KEY_PLAY:
        print("entering play sequence...")
        play()

    elif key == keys.AllKeys.KEY_NUMPAD:
        num = keys.numpad()
        print(f"inputed: {num}")

    elif key == keys.AllKeys.KEY_HELP:
        keys.help()

    elif key == keys.AllKeys.KEY_MANUAL:
        print("entering manual movement...")
        Mov.manual()


    elif key == keys.AllKeys.KEY_QUIT: # confirm to quit 
        print(f"confirm to quit ({keys.AllKeys.KEY_CONFIRM})")
        key = keys.scanKeys()
        if key == keys.AllKeys.KEY_CONFIRM:
            print("confirmed")
            key = keys.AllKeys.KEY_QUIT # confirmed quit (set back to confirmed...)
    else:
        print(key)



print("quitting")

"""end sequence"""
Img.end()