import numpy as np
import cv2
#import time

#from packaging.tags import interpreter_version

from constans import Constants
Cons = Constants()

def invert(x, max_val:int):
    return (max_val - 1) - x

class Image:
    def __init__(self):
        self.cameraIndex = 0
        print(f"opening camera {self.cameraIndex}...")
        self.cap = cv2.VideoCapture(self.cameraIndex)  # Change index if using a USB camera (/dev/video1, etc.)


        print("checking if cam is opened...")
        if not self.cap.isOpened():
            
            raise SystemError("Error: Cannot access the camera")
        else:
            print("cam OK")


    def order_points(self, pts):
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


    def warp_frame_to_rectangle(self, frame, src_points):
        # Order the points correctly
        src_points = self.order_points(src_points)
        
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


    def split_into_grid(self, image, rows : int, cols : int):
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


    def select_frames(self, frames: list):
        newFrames = []
        for frame, i in zip(frames, Cons.remove_white_space):
            if i == 1:
                newFrames.append(frame)
        return newFrames
    
    def transform_list(self, letter_list: list):
        ll = letter_list # crate copy of list IDK if needed
        choose =[]
        grid = {}
        for _ in range(7): # extract first 7 letters 
            choose.append(ll.pop(0))
        """
        Invert grid here so the 0|0 is left down
        """
        i = 0
        for y in range(Cons.rows):
            for x in range(Cons.cols):
                x = invert(x, Cons.cols)
                y = invert(y, Cons.rows)
                grid[x, y] = ll[i]
                i += 1

        return choose, grid
    
    def get_transformed_frame(self):

        
        while True:
            print("capturing frame")
            ret, frame = self.cap.read()

            if not ret:
                print("Error: Failed to capture frame: ERROR")
                return
            else:
                print("frame captured: OK")

            # Convert the frame to grayscale and readable format
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            src_points = np.array(Cons.Image.extractAllPoints, dtype=np.float32)
            frame = self.warp_frame_to_rectangle(frame, src_points) # wrap
            return frame # return the cropped frame

    
    def show_grid(self, grid: dict, choose=None, rows=10, cols=15):

        if choose is None:
            choose = []
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
    

    def end(self):
        self.cap.release()
