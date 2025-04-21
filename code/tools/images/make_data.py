import cv2 
import os 
import datetime
import random
import numpy as np
from image import Image
from constans import Constants
Img = Image()
Cons = Constants()
"""
    extractAllPoints = [(103, 17), (479, 9), (485, 464), (104, 465)]# haha markers are not working

    
# Detect ArUco markers in the frame

print("looking for marks")

# If markers are detected


    
if len(extractAllPoints) == 4:
    print("all 4 marks found: OK")
    src_points = np.array(extractAllPoints, dtype=np.float32)
    frame = self.warp_frame_to_rectangle(frame, src_points) # wrap 

"""

letters = ["_", 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
perLetter = 100

extractAllPoints = [(64, 87), (493, 68), (508, 426), (76, 443)]# haha markers are not working

current = "_"
save_dir = "/home/malina/sb/scrabblebot/code/networks/letters/val/_"

def ItemsInDir(path: str):
    # List all items (files and subdirectories) in the folder
    items = os.listdir(path)

    # Count the number of items
    return len(items)
    

while True:
    ret, frame = Img.cap.read()
    if not ret:
        print("Failed to read from camera.")
        break
    
    # Display the current video frame
    cv2.imshow("Live Feed", frame)

    
    src_points = np.array(extractAllPoints, dtype=np.float32)
    
    frame = Img.warp_frame_to_rectangle(frame, src_points) # wrap 
    
    frame_r = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    
    cv2.imshow("Live Feed_r", frame_r)
    
    frames = Img.split_into_grid(frame_r, Cons.rows, Cons.cols)
    
    frames = Img.selectFrames(frames)

    

    if False:
        for n, frame in enumerate(frames):
            print(n)
            cv2.imshow(str(n), frame)

    
    # Check for akeyboard presses
    key = cv2.waitKey(1) & 0xFF
    
    # If 'c' is pressed, capture and save the image
    if key == ord(' '):
        for n, frame in enumerate(frames):
            # Use current date/time for the filename
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{current}:{timestamp}_:_{random.randint(0,99)}.jpg"
            filepath = os.path.join(save_dir, filename)
            # Save the captured frame    
            cv2.imwrite(filepath, frame)
            print(f"Saved {filepath}")
            print(f"in {current} are {ItemsInDir(save_dir)}")
        
        # If 'q' is pressed, quit the loop
    elif key == ord('q'):
        print("Exiting...")
        break

# Release the camera and close the window
Img.cap.release()
cv2.destroyAllWindows()
