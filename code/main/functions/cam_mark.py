import cv2
#print(cv2.__version__)
#import numpy as np

def get_hand_mark(frame, detector):
    # Load the predefined dictionary

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect markers
    corners, ids, rejected = detector.detectMarkers(gray)
    if False:
        print("")
        print(corners)
        print(rejected)
        print("")
    if ids is not None:
        print(len(ids))

    #Draw detected markers on the original frame
    cv2.aruco.drawDetectedMarkers(frame, corners, ids)

    #cv2.imshow("with markers", frame)

    return frame
