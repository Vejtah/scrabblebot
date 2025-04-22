import cv2 
import os 
import datetime
import random
import numpy as np

from image import Image
from constans import Constants
from shit import SHIT
from make_black_values import Data

Dta = Data()
Sht = SHIT()
Img = Image()
Cons = Constants()

black_data = {

}


letters = ["_", 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
perLetter = 100

extractAllPoints = [(64, 87), (493, 68), (508, 426), (76, 443)]# haha markers are not working

current = "A"
save_dir = "/home/vpalaga/orgs/vp/sb/scrabblebot/code/networks/letters/train/" + current
#s

def save_data(data:float, type:str)->None:
    current_data = Dta.load()  # load current json
    current_data[type].append(data)  # add vaule
    Dta.write(current_data)  # save


def ItemsInDir(path: str):
    # List all items (files and subdirectories) in the folder
    items = os.listdir(path)

    # Count the number of items
    return len(items)


def save_frame(frame_f, extra) -> None:
    global current, save_dir
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{current}:{timestamp}_:_{extra}.jpg"
    filepath = os.path.join(save_dir, filename)
    # Save the captured frame
    #cv2.imwrite(filepath, frame_f)
    print(f"Saved {filepath}")
    #print(f"in {current} are {ItemsInDir(save_dir)}")

tile = 0
try:
    print(ItemsInDir(save_dir))

except FileNotFoundError:  # create the subfolder if it doesnt exist
    os.makedirs(save_dir, exist_ok=True)
    print(f"made {save_dir}")

while True:
    ret, frame = Img.cap.read()
    if not ret:
        print("Failed to read from camera.")
        break
    
    # Display the current video frame
    #cv2.imshow("Live Feed", frame)

    
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

    frame = frames[tile]  # get the current frame
    cv2.imshow("letter", frame)

    # Check for akeyboard presses
    key = cv2.waitKey(1) & 0xFF
    
    # If 'c' is pressed, capture and save the image
    if key == ord(' '):
        if False: # capture all tiles at one (use for whitespace images)
            for n, frame in enumerate(frames):
                letter, resized = Sht.extract_letter(frame)
                black_prc = Sht.get_black_pixel_percentage(resized)
                print(letter)
                print(black_prc)
                # types: letters, None

                save_data(black_prc, "None")


            # If 'q' is pressed, quit the loop
        else:  # use to get the individual images of letters

            #save_frame(frame, tile)

            """
            shit usage
            """
            resized = Sht.resize(frame)
            black_prc = Sht.get_black_pixel_percentage(resized)
            letter = Sht.extract_letter(resized, black_prc)

            print(f"letter: {letter}")
            print(f"black_prc: {black_prc}")
            # types: letters, None

            #save_data(black_prc, "letters")
            tile += 1

    elif key == ord('q'):
        print("Exiting...")
        break

# Release the camera and close the window
Img.cap.release()
cv2.destroyAllWindows()
