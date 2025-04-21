import time
from tqdm import tqdm

""" split into Classes"""
"""__init__"""

from movement import Movement
from constans import Constants
from shit import SHIT
from keys import Keys
from image import Image
from alg import Scrabble

Mov = Movement()  # movement from Movement
Cons = Constants()
shit = SHIT()
keys = Keys()
Img = Image()
s = Scrabble()

Mov.release() #  release the motors

"""play def"""

# have to have the function here bc methods shouldnt be calling other methods in the same class
def move_to(target_x: int, target_y: int):
    Mov.move(move_to(target_x, target_y))

def move_to_piece(x, y):
    move_to(Mov.move_to_piece(x, y))

def ret() -> None:
    move_to_piece(14, 10)
    time.sleep(Mov.sleep)
    move_to(0, 0)
    Mov.move(-5, -5)
    Cons.s_x, Cons.s_y = 0, 0 # reset the x and y var
    #Mov.open() # open the hand
    
    
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
        letters.append(shit.SHIT(frame))  # use network
        time.sleep(0.005)  # remove (simulate the loading)
    
    print("transforming into a dict")
    
    choose, grid = Img.transformList(letters)
    return grid, choose

def best_word(grid, choose):
    global Cons  # get curent moves  - may be an error
    
    best_move, _ = s.eval_moves(s.all_possible_moves(grid, choose, Cons.played_moves))
    
    # detect if theher arent any avlb words
    
    
    try:
        w = best_move[0]  # try to get the word
    except TypeError:
        print("cought")
        return 0  #  code catch
    
    return best_move


def grab_letter(letter_pos) -> None:
    move_to_piece(14, 10)
    time.sleep(0.5)
    letter_x_pos = letter_pos * 2  # gaps between holders
    
    move_to_piece(letter_x_pos, 10)
    time.sleep(0.5)
    
    move_to_piece(letter_x_pos, 11)  # slide on to the tile
    
    Mov.close()
    time.sleep(0.5)
    
    move_to_piece(letter_x_pos, 10)  # move out
    


def build_word(move_tupple, choose: list) -> str | None:  # depending on if the bot lost or not
    
    letters_dict = move_tupple[3]
    
    for (x, y), letter in letters_dict.items():

        letter_pos = choose.index(letter)
        
        grab_letter(letter_pos)
        
        move_to_piece(x, y)
        Mov.open()

        ret()  # return to start and calib

def play():
    grid, choose = GetGrid()
    Img.show_grid(grid, choose)
    
    word = best_word(grid, choose)
    if word == 0:
        return 0
    
    Cons.played_moves.append(word[0])  # add word to played moves
    build_word(word, choose)
    return 1
    

"""main loop"""
print("entering main loop...")

print("opening hand...")

Mov.open() # open the hand in the start
    
#  use try to use fimnally to release motors
try:
    key = ""           
    while key != keys.AllKeys.KEY_QUIT:

        print(f"press keys to continue, for help press {keys.AllKeys.KEY_HELP}...")
        key = keys.scanKeys()

        if key == keys.AllKeys.KEY_PLAY:
            print("entering play sequence...")
            if play() == 0:
                print("the bot has lost")
                break
        elif key == keys.AllKeys.KEY_NUMPAD:
            num = keys.numpad()
            print(f"inputed: {num}")

        elif key == keys.AllKeys.KEY_HELP:
            keys.help()

        elif key == keys.AllKeys.KEY_MANUAL:
            print("entering manual movement...")
            Mov.manual()
            Mov.release()


        elif key == keys.AllKeys.KEY_QUIT: # confirm to quit 
            print(f"confirm to quit ({keys.AllKeys.KEY_CONFIRM})")
            key = keys.scanKeys()
            if key == keys.AllKeys.KEY_CONFIRM:
                print("confirmed")
                key = keys.AllKeys.KEY_QUIT # confirmed quit (set back to confirmed...)
        else:
            print(key)
            
#except Exception as e:
    #print(e)
    
finally:
    Mov.release()
    Img.end()

print("quitting")

"""end sequence"""
