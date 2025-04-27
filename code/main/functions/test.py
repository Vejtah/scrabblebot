import os
print(os.getcwd())

import cv2

from cam_mark import get_hand_mark

try:
    from config import Constants
except ModuleNotFoundError:
    from functions.config import Constants

import image as Img

h, w = Img.get_cam_res(cam_index=2)

cameraIndex = Constants.System.camera_index
cap = cv2.VideoCapture(cameraIndex)

  # Change index if using a USB camera (/dev/video1, etc.)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)

ret, frame = cap.read()
if ret:
    pass
else:
    print("Failed to capture frame.")

# Set the desired resolution

# Verify if the settings were applied

aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
parameters = cv2.aruco.DetectorParameters()

# Create the ArUco detector
detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)

pos = [(189, 206), (943, 178), (965, 803), (207, 829)]

while True:


    ret, frame = cap.read()
    cv2.imshow("org", frame)
    # cv2.imshow(str(random.randint(0, 100)), frame)
    if not ret:
        print("Error: Failed to capture frame: ERROR")
    else:
        pass
    frame = get_hand_mark(frame, detector)

    cv2.imshow("mark", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
