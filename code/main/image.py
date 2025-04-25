import numpy as np
import cv2
#import time
#from packaging.tags import interpreter_version


from constants import Constants

def invert(x, max_val:int):
    return (max_val - 1) - x

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


def select_frames(frames: list):
    newFrames = []
    for frame, i in zip(frames, Constants.remove_white_space):
        if i == 1:
            newFrames.append(frame)
    return newFrames

def transform_list(letter_list: list):
    ll = letter_list # crate copy of list IDK if needed
    choose =[]
    grid = {}
    #print(f"len ll: {len(ll)}")
    for _ in range(7): # extract first 7 letters 
        choose.append(ll.pop(0))
    #print(f"len ll: {len(ll)}")

    """
    without inverting y the 0|0 is left top
    Invert y grid here so the 0|0 is left down
    """
    i = 0
    for y in range(Constants.rows - 2): # remove the 2 rows of not grid
        
        y = invert(y, Constants.rows - 2)

        for x in range(Constants.cols):

            #print(i)
            if i == 150:
                    print(x, y) 
            grid[x, y] = ll[i]
            
            i += 1

    return choose, grid

def get_transformed_frame():

    """
    the camera needs to be initialized everytime you take a picture,
    if it doesn't do so and only at the start of the program, than if
    you want to take a new picture it needs 3 times until it actually
    refreshes the frame and outputs the actual current frame.
    I have spent 2 hours finding this shit out, so you are welcome :D
    -Vejtah
    """

    cameraIndex = Constants.System.camera_index

    while True:
        print("capturing frame...")
        
        cap = cv2.VideoCapture(cameraIndex)  # Change index if using a USB camera (/dev/video1, etc.)


        print("checking if cam is opened...")
        if not cap.isOpened():
        
            raise SystemError("Error: Cannot access the camera")
        else:
            print("cam OK")
        
        ret, o_frame = cap.read()
        #cv2.imshow(str(random.randint(0, 100)), frame)
        if not ret:
            print("Error: Failed to capture frame: ERROR")
            return
        else:
            print("frame captured: OK")

        # Convert the frame to grayscale and readable format
        
        src_points = np.array(Constants.Image.extractAllPoints, dtype=np.float32)
        frame = warp_frame_to_rectangle(o_frame, src_points) # wrap
        
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        
        return frame, o_frame # return the cropped frame and original frame


def show_grid(grid: dict,
              choose=None,
              rows=Constants.rows - 2,  # remove the top 2 lines
              cols=Constants.cols,
              i=True):  # invert around the y

    if choose is None:
        choose = []
    print("")
    line = ""
    for letter in choose:
        line += f" {letter}"
    
    if len(choose) >= 1:
        print(f"choose:{line}")

    x_line = f"xx: "

    for x in range(cols):
        x_line += f"| {x:<2}"
    print(x_line)

    for y in range(rows):
        if i:
            y = invert(y, rows)
        line = f"{y:>2}:"
        
        for x in range(cols):
            pos = grid[x, y]
            if pos is None:  # replace None with _
                pos = "_"
            line += f" | {pos}"
        print(line)
    print("")
