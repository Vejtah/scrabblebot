from string import capwords

import cv2

from cam_mark import get_hand_mark
from config import Constants
import image as Img

h, w = Img.get_cam_res(cam_index=2)

Constants.System.camera_index = 2  # get on pc
cameraIndex = Constants.System.camera_index
cap = cv2.VideoCapture(cameraIndex)

  # Change index if using a USB camera (/dev/video1, etc.)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)

ret, frame = cap.read()
if ret:
    height, width = frame.shape[:2]
    print(f"Resolution set to: {width}x{height}")
else:
    print("Failed to capture frame.")

# Set the desired resolution

# Verify if the settings were applied
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
print(f"Camera resolution set to: {int(width)}x{int(height)}")

aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
parameters = cv2.aruco.DetectorParameters()

# Create the ArUco detector
detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)

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
