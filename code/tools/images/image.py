import numpy as np
import cv2
import time

from constans import Constants
Cons = Constants()

class Image:
    def __init__(self):
        self.cameraIndex = 2
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


    def selectFrames(self, frames: list):
        newFrames = []
        for frame, i in zip(frames, Cons.remove_white_space):
            if i == 1:
                newFrames.append(frame)
        return newFrames
    
    def transformList(self, letter_list: list):
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
    
    def GetTransformedFrame(self): 

        
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
                frame = self.warp_frame_to_rectangle(frame, src_points) # wrap 
                return frame # return the croped frame
            
            else:
                print(f"only {len(extractAllPoints)} markes found: ERROR")
                time.sleep(0.5) # wait 0,5 s before reattempting to find all markers
                print("trying again...")

    
    def show_grid(self, grid: dict, choose: list = [], rows=10, cols=15):

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






