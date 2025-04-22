def white_space_start():
    j = 101010101010100000000000000000  # first 2 lines
    j = [int(i) for i in str(j)]  # turn int to list
    remove_white_space = j
    for _ in range(10 * 15):
        remove_white_space.append(1)  #
    return remove_white_space


class Constants:  #
    def __init__(self):
        pass

    print("creating pos variables...")

    class Pos:
        # hand
        grabber = 0

        # main
        s_x = 0
        s_x_max = 665

        x_start_offset = 10  #
        x_end_offset = 10

        s_y = 0
        s_y_max = 760

        y_start_offset = 15
        y_end_offset = 5

    class System:
        root_dir = "/home/malina/sb/scrabblebot/code/main/"
        keyboardName = "Logitech USB Keyboard"
        json_path = "black_values.json"
        rasp_pi_ports = 10  # amt of ports to search for devices

    # create the map

    remove_white_space = white_space_start()

    pointsPositions = [1, 0, 3, 2]
    rows, cols = 10 + 2, 15  # 10 for grid and 2 for use pieces

    class Image:
        available_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        add_black_prc = 10  # use if the letter recognition isn't working properly
        extractAllPoints = [(64, 87), (493, 68), (508, 426), (76, 443)]

    played_moves = []  # list to store all played moves

