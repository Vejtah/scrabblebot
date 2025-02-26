import cv2
import numpy as np
import time
from evdev import InputDevice, categorize, ecodes
import board
from adafruit_motor import stepper
from adafruit_motorkit import MotorKit
from tqdm import tqdm
"""define"""
# Load the predefined ArUco dictionary

print("defining keys...")

class Keys: # class for all contorols

    KEY_PLAY = "KEY_SPACE"
    KEY_QUIT = "KEY_Q"
    KEY_CONFIRM = "KEY_ENTER"
    KEY_MOVE_Xp = "KEY_RIGHT" # x to right 
    KEY_MOVE_Xn = "KEY_LEFT" # x to left
    KEY_MOVE_Yp = "KEY_UP" # y up
    KEY_MOVE_Yn = "KEY_DOWN" # y down
    KEY_HELP = "KEY_H"
    KEY_NUMPAD = "KEY_N"
    KEY_MANUAL = "KEY_M"

MANUAL_MOVMENT = [Keys.KEY_MOVE_Xp, Keys.KEY_MOVE_Xn, Keys.KEY_MOVE_Yp, Keys.KEY_MOVE_Yn]

print("creating pos variables...")

class Pos:
    grabber = 0
    s_x = 0
    s_x_max = 1000 # find
    
    s_y = 0
    s_y_max = 1000

numPad = {
    "KEY_KP0": 0,
    "KEY_KP1": 1,
    "KEY_KP2": 2,
    "KEY_KP3": 3,
    "KEY_KP4": 4,
    "KEY_KP5": 5,
    "KEY_KP6": 6,
    "KEY_KP7": 7,
    "KEY_KP8": 8,
    "KEY_KP9": 9
}
print("initilasing stepper...")

kit = MotorKit(i2c=board.I2C())
s_x = kit.stepper1
s_y = kit.stepper2
sleep = .03

print("defining constans...")

pointsPositions = [1, 0, 3, 2]
rows, cols = 10 + 2, 15 # 10 for grid and 2 for use pieces

# create the map
j = 101010101010100000000000000000 # first 2 lines
j = [int(i) for i in str(j)] # turn int to list 
remove_white_space = j
for _ in range(10 * 15):
    remove_white_space.append(1)



print("defining keyboard sence...")
device = InputDevice('/dev/input/event4')
print(f"Listening on {device.path} - {device.name} : OK")

"""__init__"""


# Open the camera
cameraIndex = 0
print(f"opening camera {cameraIndex}...")
cap = cv2.VideoCapture(cameraIndex)  # Change index if using a USB camera (/dev/video1, etc.)


"""prechecks"""


print("checking if cam is opened...")
if not cap.isOpened():
    print("Error: Cannot access the camera")
else:
    print("cam OK")


"""functions"""
print("checking functions")
#  funtions for image processing 

def order_points(pts):
    # Order points: top-left, top-right, bottom-right, bottom-left
    pts = np.array(pts, dtype="float32")
    s = pts.sum(axis=1)
    diff = np.diff(pts, axis=1)
    
    ordered = np.zeros((4, 2), dtype="float32")
    ordered[0] = pts[np.argmin(s)]      # top-left has the smallest sum
    ordered[2] = pts[np.argmax(s)]      # bottom-right has the largest sum
    ordered[1] = pts[np.argmin(diff)]   # top-right has the smallest difference
    ordered[3] = pts[np.argmax(diff)]   # bottom-left has the largest difference
    return ordered


def warp_frame_to_rectangle(frame, src_points):
    # Order the points correctly
    src_points = order_points(src_points)
    
    # Compute width of new image
    widthA = np.linalg.norm(src_points[2] - src_points[3])
    widthB = np.linalg.norm(src_points[1] - src_points[0])
    maxWidth = int(max(widthA, widthB))
    
    # Compute height of new image
    heightA = np.linalg.norm(src_points[1] - src_points[2])
    heightB = np.linalg.norm(src_points[0] - src_points[3])
    maxHeight = int(max(heightA, heightB))
    
    # Destination points are the corners of the new rectangle
    dst_points = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]
    ], dtype=np.float32)
    
    # Compute perspective transformation matrix
    matrix = cv2.getPerspectiveTransform(src_points, dst_points)
    warped_frame = cv2.warpPerspective(frame, matrix, (maxWidth, maxHeight))
    
    return warped_frame


def split_into_grid(image, rows : int, cols : int):
    """
    Splits an image into a grid of specified rows and columns.

    Parameters:
    - image: The image/frame to split (numpy array).
    - rows: Number of rows in the grid.
    - cols: Number of columns in the grid.

    Returns:
    - grid_parts: A list of sub-images (grid parts).
    """
    height, width, _ = image.shape
    row_height = height / rows
    col_width = width / cols

    grid_parts = [
        image[round(i * row_height):round((i + 1) * row_height), round(j * col_width):round((j + 1) * col_width)]
        for i in range(rows)
        for j in range(cols)
    ]
    return grid_parts


def selectFrames(frames: list):
    newFrames = []
    for frame, i in zip(frames, remove_white_space):
        if i == 1:
            newFrames.append(frame)
    return newFrames


def SHIT(frame):

    pass
    return "s" 


def transformList(letter_list: list):
    ll = letter_list # crate copy of list idk if needed
    choose =[]
    grid = {}
    for _ in range(7): # extract first 7 letters 
        choose.append(ll.pop(0))
    
    i = 0
    for y in range(10):
        for x in range(15):
            grid[x, y] = ll[i]
            i += 1

    return choose, grid


def scanKeys():
    for event in device.read_loop():
        if event.type == ecodes.EV_KEY:
            key_event = categorize(event)
            if key_event.keystate == key_event.key_down:
                # Sometimes key_event.keycode might be a list; handle both cases.

                key = key_event.keycode

                return key
                break


def numpad():
    print("entering numpad...")
    num = ""
    key = ""
    while key != Keys.KEY_CONFIRM:
        key = scanKeys()
        if key in numPad:
            num += str(numPad[key])
            print(num)
        
    return int(num)


def help():


    print("help:")
    for attr, value in Keys.__dict__.items():
        if not attr.startswith('__'):
            print(f"{attr} = {value}")
    print("")


def show_grid(grid: dict, choose: list = [], rows=10, cols=15):

    print("")
    line = ""
    for letter in choose:
        line += f" {letter}"
    
    if len(choose) >= 1:
        print(f"choose:{line}")

    for y in range(rows):
        line = ""
        for x in range(cols):
            line += f" | {grid[x, y]}"
        print(line)
    print("")


def GetTransformedFrame(): 

    
    while True:
        print("capturing frame")
        ret, frame = cap.read()

        if not ret:
            print("Error: Failed to capture frame: ERROR")
            return
        else:
            print("frame captured: OK")

        # Convert the frame to grayscale and readable format
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        if False:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            denoised_frame = cv2.fastNlMeansDenoisingColored(frame, None, h=10, hColor=10, templateWindowSize=7, searchWindowSize=21)

            hsv = cv2.cvtColor(denoised_frame, cv2.COLOR_BGR2HSV)
        else:
            extractAllPoints = [(103, 17), (479, 9), (485, 464), (104, 465)]# haha markers are not working

            
        # Detect ArUco markers in the frame

        print("looking for marks")
        
        # If markers are detected
        

            
        if len(extractAllPoints) == 4:
            print("all 4 marks found: OK")
            src_points = np.array(extractAllPoints, dtype=np.float32)
            frame = warp_frame_to_rectangle(frame, src_points) # wrap 
            return frame # return the croped frame
        
        else:
            print(f"only {len(extractAllPoints)} markes found: ERROR")
            time.sleep(0.5) # wait 0,5 s before reattempting to find all markers
            print("trying again...")
            

def move(x_moveby: int, y_moveby: int):

    if 0 <= (Pos.s_x + x_moveby) <= Pos.s_x_max:
        print("move X pos: OK")
    else:
        print("move X unable: ERROR")
        return


    if 0 <= (Pos.s_y + y_moveby) <= Pos.s_y_max:
        print("move Y pos: OK")
    else:
        print("move Y unable: ERROR")
        return


    if x_moveby >= 0:
        x_dir = stepper.FORWARD
        x_dir_i = 1

    else:
        x_dir = stepper.BACKWARD
        x_moveby *= -1
        x_dir_i = -1


    if y_moveby >= 0:
        y_dir = stepper.FORWARD
        y_dir_i = 1

    else:
        y_dir = stepper.BACKWARD
        y_moveby *= -1
        y_dir_i = -1

    x_progress = tqdm(total=x_moveby, desc="X move Progress")
    y_progress = tqdm(total=y_moveby, desc="Y move Progress")

    # combine x and y movement:
    while x_moveby >= 1 and y_moveby >= 1:
        
        s_x.onestep(direction=x_dir)
        time.sleep(sleep / 2) # wait 1/2 of waiting cycle

        s_y.onestep(direction=y_dir)

        x_progress.update(1)
        y_progress.update(1)

        x_moveby -= 1
        y_moveby -= 1

        Pos.s_x += x_dir_i # update location +1 if pos else -1
        Pos.s_y += y_dir_i

        time.sleep(sleep / 2)

    if x_moveby >= y_moveby:
        x_left = x_moveby - y_moveby

        for _ in range(x_left):
            s_x.onestep(direction=x_dir)

            x_progress.update(1)

            Pos.s_x += x_dir_i

            time.sleep(sleep)

    else:
        y_left = y_moveby - x_moveby

        for _ in range(y_left):
            s_y.onestep(direction=x_dir)

            y_progress.update(1)

            Pos.s_y += y_dir_i

            time.sleep(sleep)
    
    s_x.release() # release to prevent overheat
    s_y.release()
            

def move_to(target_x: int, target_y: int):
    x_moveby = target_x - Pos.s_x
    y_moveby = target_y - Pos.s_y

    # check if move possible

    x_next = Pos.s_x - x_moveby
    y_next = Pos.s_y - y_moveby

    if x_next >= 0 and y_next >= 0:
        print("move possible, proceeding...")
    else:
        print("next move calced in minus: ERROR")
        print("aborting...")
        return
    
    move(x_moveby, y_moveby)



def MaualMovement(key: int, amt=5):

    action = MANUAL_MOVMENT.index(key)
    """
    0 = x+
    1 = x-
    2 = Y+
    3 = Y-
    """

    if action == 0:
        move(amt, 0)
        print("moving x+")
    elif action == 1:
        move(-1 * amt, 0)
        print("moving x-")
    elif action == 2:
        move(0, amt)
        print("moving y+")
    elif action == 3: 
        move(0, amt * -1)
        print("moving y-")

    print("current X Y pos:")
    print(f"{Pos.s_x} | {Pos.s_y}")


def manual():
    print("entering maual movement...")
    print("")
    print("select step: (int)")
    step = numpad()
    
    print(f"step: {step}")
    print("move with keys...")

    key =""
    while key != Keys.KEY_QUIT:
        key = scanKeys()
        if key in MANUAL_MOVMENT:
            MaualMovement(key, amt=step)
    print("exiting manual...")


"""main functions"""


"""play def"""

def GetGrid():
    print("transforing frame...")
    transformedFrame = GetTransformedFrame()

    print("spliting frame...")
    frames = split_into_grid(transformedFrame, rows, cols)

    print("selecting frames...")
    frames = selectFrames(frames)

    # preform a check 
    if len(frames) == 157:
        print("Frame Selection : OK")
    else:
        print("Error in split or select: ERROR")
        return # add a returnpoint IDK

    print("transforming frames to string...")
    letters = []
    i = 0
    for frame in tqdm(frames, desc="img to str"):
        letters.append(SHIT(frame))
        time.sleep(0.005)
    
    print("transforming into a dict")
    
    choose, grid = transformList(letters)
    return grid, choose


def play():
    grid, choose = GetGrid()
    show_grid(grid, choose)
    

"""main loop"""
print("entering main loop...")


key = ""            
while key != Keys.KEY_QUIT:

    print(f"press keys to continue, for help press {Keys.KEY_HELP}...")
    key = scanKeys()

    if key == Keys.KEY_PLAY:
        print("entering play sequence...")
        play()

    elif key == Keys.KEY_NUMPAD:
        num = numpad()
        print(f"inputed: {num}")

    elif key == Keys.KEY_HELP:
        help()

    elif key == Keys.KEY_MANUAL:
        print("entering manual movement...")
        manual()


    elif key == Keys.KEY_QUIT: # confirm to quit 
        print(f"confirm to quit ({Keys.KEY_CONFIRM})")
        key = scanKeys()
        if key == Keys.KEY_CONFIRM:
            print("confirmed")
            key = Keys.KEY_QUIT # confirmed quit
    else:
        print(key)

print("quitting")

"""end sequence"""

cap.release()
