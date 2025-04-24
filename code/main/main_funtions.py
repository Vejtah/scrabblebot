import time
#from wsgiref.util import request_uri
import cv2
from setuptools.unicode_utils import try_encode
#from pipenv.pep508checker import implementation_name
from tqdm import tqdm

import shit as sh
import data as d
import image as img

import alg
from movement import Movement
from constants import Constants
Mov = Movement()
s = alg.Scrabble()

def shit(frame, bw=None) -> str | None:

    """
    Shit stands for:
        Swift
        High-res.
        Image
        Transformer
    """

    resized = sh.resize(frame)
    black_prc = sh.get_black_pixel_percentage(resized, bw=bw)

    if sh.is_letter(black_prc):
        # cv2.imshow("letter", frame)
        letter = sh.extract_letter(resized)
        # print(letter)
        d.add_black_letter_val(black_prc)
        return letter
    return None


def get_grid():
    print("->Frame")
    transformed_frame = img.get_transformed_frame()
    # cv2.imshow("trans", transformed_frame)
    print("splitting frame...")
    frames = img.split_into_grid(transformed_frame, Constants.rows, Constants.cols)

    print("selecting frames...")
    frames = img.select_frames(frames)

    # preform a check
    if len(frames) == 157:
        print("Frame Selection : OK")
    else:
        print("Error in split or select: ERROR")
        return  # add a return point IDK

    print("->transforming frames to string...")
    letters = []

    bw = None  # declare bw
    # can use adaptive lightning

    gray = cv2.cvtColor(transformed_frame, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("gray", gray)

    if Constants.Image.use_adaptive_lightning:
        bw = cv2.adaptiveThreshold(
            gray, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            blockSize=11,  # neighborhood size
            C=2  # constant subtracted from mean
        )

    prc_of_black_view = sh.get_black_pixel_percentage(gray, d=False)

    mid = d.clac_midpoint(d.load(Constants.System.json_path_black_vals))

    print(f"->mid point: {round(mid, ndigits=2)}")
    print(f"->percent of black in the whole frame: {round(prc_of_black_view, ndigits=2)}")
    print("")
    for frame in tqdm(frames, desc="img to str"):  # use tqdm to crate a loading bar

        letters.append(shit(frame, bw=bw))  # use network
    print("")
    print("transforming into a dict")

    choose, grid = img.transform_list(letters)
    return grid, choose


def best_word(grid, choose, played_moves):

    best_move, _ = alg.eval_moves(s.all_possible_moves(grid, choose, played_moves))

    # detect if there aren't any available words

    try:
        _ = best_move[0]  # try to get the word
    except TypeError:
        print("caught")
        return 0  # code catch

    return best_move


def grab_letter(letter_pos) -> None:
    Mov.move_to_piece(14, 10)
    time.sleep(0.5)
    letter_x_pos = letter_pos * 2  # gaps between holders

    Mov.move_to_piece(letter_x_pos, 10)

    Mov.open()
    time.sleep(0.5)

    Mov.move_to_piece(letter_x_pos, 11.5)  # slide on to the tile

    Mov.close()
    time.sleep(0.5)

    Mov.move_to_piece(letter_x_pos, 10)  # move out


def build_word(move_tuple, choose: list) -> str | None:  # depending on if the bot lost or not

    letters_dict = move_tuple[3]

    for (x, y), letter in letters_dict.items():
        letter_pos = choose.index(letter)

        grab_letter(letter_pos)

        Mov.move_to_piece(x, y)
        Mov.open()

        Mov.ret()  # return to start and calib


def plot_word(move_tuple: tuple, grid:dict) -> None:

    letters_dict = move_tuple[3]

    for (x, y), letter in letters_dict.items():
        grid[(x, y)] = letter.upper()  # add the letter to the main dict


def play(played_moves):
    tried_times = 0

    if Constants.Image.transform_img_times < 1:
        d.log("transform times if lower than 1: unable to transform any images", t=1)

        return

    while tried_times != Constants.Image.try_times_to_recognise:
        for _ in range(Constants.Image.transform_img_times):
            # save data to a json file and compare at the end to output a val
            grid, choose = get_grid()
            d.add_grid(grid, choose)

        err_g, err_ch = d.compare_grids()


        if err_g == 0 and err_ch == 0:
            print("resetting grid")
            d.reset_grids()

            img.show_grid(grid, choose)
            break

        else:
            d.log(f"failed to recognise the grid, i: {tried_times}", t=1)
            d.reset_grids() # reset the json with grids
            print("trying again...")
            tried_times += 1


    if tried_times >= Constants.Image.try_times_to_recognise:
        d.log(f"failed to rec the grid {Constants.Image.try_times_to_recognise} times giving up", t=2)
        print("giving up...")
    # print(grid)
    # print(choose)

    for letter in choose:  # check if all choose letters are existing
        if letter is None:
            return 2

    word = best_word(grid, choose, played_moves)
    print("word")
    d.log("word:", word)
    print(word)
    plot_word(word, grid)

    img.show_grid(grid, i=True)
    img.show_grid(grid, i=False)

    if word == 1:
        return 1

    played_moves.append(word[0])  # add word to played moves
    #build_word(word, choose)

    return 0
