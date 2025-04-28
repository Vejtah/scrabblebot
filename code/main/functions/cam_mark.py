import cv2
#print(cv2.__version__)
#import numpy as np

def get_hand_mark(frame, detector):
    # Load the predefined dictionary

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Detect markers
    corners, ids, rejected = detector.detectMarkers(gray)

    try:
        pts = corners[0].reshape((4, 2))
        # compute mean of x’s and y’s
        center = pts.mean(axis=0)
        cx, cy = int(center[0]), int(center[1])

        # draw it
        cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)
        return cx, cy, frame

    except IndexError:
        return None, None, frame
