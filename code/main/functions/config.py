import os

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


    class System:
        current_file = os.path.abspath(__file__)
        current_folder = os.path.dirname(current_file)
        root_dir = os.path.dirname(current_folder)
        print(f"root: {root_dir}")

        json_path_black_vals =r"functions/json/black_values.json"
        rasp_pi_ports = 10  # amt of ports to se arch for devices
        log_path = r"logs/.log.txt"
        log_time_format = "%d.%m.%y-%H.%M.%S"

        raspberry_name = "malina"


        running_on_raspberry = False
        if raspberry_name in root_dir.split("/"):  # detect if running on raspberry or not
            running_on_raspberry = True
            print(f"running on pi")
        else:
            print(f"running on PC")

        if running_on_raspberry:
            camera_index = 0  # find your camera
            keyboardName = "Logitech USB Keyboard"  # you can set different keyboards on pc and pi
        else:
            camera_index = 2
            keyboardName = "Logitech USB Receiver"

        print(f"cam index: {camera_index}")


    class Image:
        available_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        add_black_prc = 0  # use if the letter recognition isn't working properly
        """
        extract all points depends on your camera resolution
        """
        #extractAllPoints = [(64, 87), (493, 68), (508, 426), (76, 443)] for default cv2 cam res -> bad cam quality
        extractAllPoints = [(189, 206), (943, 178), (965, 803), (207, 829)]

        use_adaptive_lightning = False
        transform_img_times = 2
        compare_grids_json = r"functions/json/grid_choose.json"
        try_times_to_recognise = 3
        check_multiple_times = True
        imshow_loadtime = 1  # ms



    class Test:
        choose = ["F", "W", "B", "G", "D", "V", "C"]
        testing_mode = True  # testing modus

    played_moves = []  # list to store all played moves

    # create the map

    remove_white_space = white_space_start()

    pointsPositions = [1, 0, 3, 2]
    rows, cols = 12, 15  # 10 for grid and 2 for use pieces

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
