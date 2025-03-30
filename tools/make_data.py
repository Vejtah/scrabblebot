import cv2 
import os 
import datetime
import random


cap = cv2.VideoCapture(1) 

letters = ["_", 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
perLetter = 100

current = "headphones"
save_dir = "C:/Users/vit/myenv/code/dataset/check/"

def ItemsInDir(path: str):
    # List all items (files and subdirectories) in the folder
    items = os.listdir(path)

    # Count the number of items
    return len(items)



while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to read from camera.")
        break
    
    # Display the current video frame
    cv2.imshow("Live Feed", frame)
    
    # Check for akeyboard presses
    key = cv2.waitKey(1) & 0xFF
    
    # If 'c' is pressed, capture and save the image
    if key == ord(' '):
        # Use current date/time for the filename
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{current}{timestamp}_{random.randint(0,99)}.jpg"
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
cap.release()
cv2.destroyAllWindows()
