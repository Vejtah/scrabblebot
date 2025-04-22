import time
from tqdm import tqdm

""" split into Classes"""

from movement import Movement
from constans import Constants
from shit import SHIT
from keys import Keys
from alg import Scrabble

"""__init__"""

Mov = Movement()  # movement from Movement
Cons = Constants()
Sht = SHIT()
keys = Keys()
s = Scrabble()

Mov.release()  # release the motors

"""play def"""

class Functions:

    def shit( frame) -> str|None:
        resized = Sht.resize(frame)
        black_prc = Sht.get_black_pixel_percentage(resized)
        if Sht.is_letter(black_prc):
            letter = Sht.extract_letter(resized, black_prc)
            return letter
        return None
    # have to have the function here bc methods shouldn't be calling other methods in the same class
    def move_to( target_x: int, target_y: int) -> None:

        x_move_by, y_move_by = Mov.move_to(target_x, target_y)

        Mov.move(x_move_by, y_move_by)

    def move_to_piece( x, y):

        x_target, y_target = Mov.move_to_piece(x, y)

        self.move_to(x_target, y_target)

    def ret() -> None:
        self.move_to_piece(14, 10)
        time.sleep(Mov.sleep)
        self.move_to(0, 0)
        Mov.move(-5, -5)
        Cons.s_x, Cons.s_y = 0, 0  # reset the x and y var
        # Mov.open() # open the hand

    def get_grid():
        print("transforming frame...")
        transformed_frame = Image.get_transformed_frame()

        print("splitting frame...")
        frames = Image.split_into_grid(transformed_frame, Cons.rows, Cons.cols)

        print("selecting frames...")
        frames = Image.select_frames(frames)

        # preform a check
        if len(frames) == 157:
            print("Frame Selection : OK")
        else:
            print("Error in split or select: ERROR")
            return  # add a return point IDK

        print("transforming frames to string...")
        letters = []

        for frame in tqdm(frames, desc="img to str"):  # use tqdm to crate a loading bar

            letters.append(self.shit(frame))  # use network

        print("transforming into a dict")

        choose, grid = Image.transform_list(letters)
        return grid, choose

    def best_word( grid, choose):
        global Cons  # get current moves  - may be an error

        best_move, _ = s.eval_moves(s.all_possible_moves(grid, choose, Cons.played_moves))

        # detect if there aren't any available words

        try:
            _ = best_move[0]  # try to get the word
        except TypeError:
            print("caught")
            return 0  # code catch

        return best_move

    def grab_letter( letter_pos) -> None:
        self.move_to_piece(14, 10)
        time.sleep(0.5)
        letter_x_pos = letter_pos * 2  # gaps between holders

        self.move_to_piece(letter_x_pos, 10)
        time.sleep(0.5)

        self.move_to_piece(letter_x_pos, 11)  # slide on to the tile

        Mov.close()
        time.sleep(0.5)

        self.move_to_piece(letter_x_pos, 10)  # move out

    def build_word( move_tuple, choose: list) -> str | None:  # depending on if the bot lost or not

        letters_dict = move_tuple[3]

        for (x, y), letter in letters_dict.items():
            letter_pos = choose.index(letter)

            self.grab_letter(letter_pos)

            self.move_to_piece(x, y)
            Mov.open()

            self.ret()  # return to start and calib
