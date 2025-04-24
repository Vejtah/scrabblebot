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

    class Pos:
        # hand
        grabber = 0

        # main - set current raw x and y pos to max at start 
        s_x_max = 665
        s_x = s_x_max

        x_start_offset = 35  #
        x_end_offset = x_start_offset

        s_y_max = 760
        s_y = s_y_max

        y_start_offset = 140
        y_end_offset = 25

    class System:
        root_dir = "/home/malina/sb/scrabblebot/code/main/"
        keyboardName = "Logitech USB Keyboard"
        json_path_black_vals = "black_values.json"
        rasp_pi_ports = 10  # amt of ports to search for devices
        camera_index = 0  # find your camera
        log_path = r".log.txt"
        log_time_format = "%d.%m.%y-%H.%M.%S"
        

    # create the map

    remove_white_space = white_space_start()

    pointsPositions = [1, 0, 3, 2]
    rows, cols = 12, 15  # 10 for grid and 2 for use pieces

    class Image:
        available_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        add_black_prc = 0  # use if the letter recognition isn't working properly
        extractAllPoints = [(64, 87), (493, 68), (508, 426), (76, 443)]
        use_adaptive_lightning = False
        transform_img_times = 2
        compare_grids_json = r"grid_choose.json"
        try_times_to_recognise = 3

    played_moves = []  # list to store all played moves

