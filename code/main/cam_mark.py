import cv2
#print(cv2.__version__)
#import numpy as np

def get_hand_mark(frame):
    # Load the predefined dictionary
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    parameters = cv2.aruco.DetectorParameters()

    # Create the ArUco detector
    detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect markers
    corners, ids, rejected = detector.detectMarkers(gray)
    print("")
    print(corners)
    print(ids)
    print(rejected)
    print("")
    #Draw detected markers on the original frame
    cv2.aruco.drawDetectedMarkers(frame, corners, ids)

    cv2.imshow("with markers", frame)

