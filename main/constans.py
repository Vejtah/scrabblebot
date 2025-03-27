

class Constants:#
    def __init__(self):
        pass
    print("creating pos variables...")

    class Pos:
        #hand
        grabber = 0

        # main
        s_x = 0
        s_x_max = 1000 # find

        x_start_offset = 10 # 
        x_end_offset = 10

        s_y = 0
        s_y_max = 1000

        y_start_offset = 15
        y_end_offset = 5

    # create the map
    def whiteSpaceStart():
        j = 101010101010100000000000000000 # first 2 lines
        j = [int(i) for i in str(j)] # turn int to list 
        remove_white_space = j
        for _ in range(10 * 15):
            remove_white_space.append(1)#
        return remove_white_space
    
    remove_white_space = whiteSpaceStart()

    pointsPositions = [1, 0, 3, 2]
    rows, cols = 10 + 2, 15 # 10 for grid and 2 for use pieces

    keyboardName = "Logitech USB Keyboard"

