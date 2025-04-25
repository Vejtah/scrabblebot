import cv2
import numpy as np

# Define the dictionary
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

# Generate and save markers with IDs 0 to 3
for marker_id in range(1):
    marker_size = 200  # Size of the marker in pixels
    marker_image = cv2.aruco.generateImageMarker(aruco_dict, marker_id, marker_size)
    filename = f"makers/marker_{marker_id}.png"
    cv2.imwrite(filename, marker_image)
    print(f"Saved {filename}")
