import os
import time
from pygame.draw_py import draw_lines

print(os.getcwd())

import cv2
import math

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
class Line:
    def __init__(self, p1:tuple[int ,int], p2):
        self.start_x, self.start_y = p1
        self.end_x,   self.end_y   = p2

        self.x = self.end_x - self.start_x
        if self.x < 0:
            self.x = self.start_x - self.end_x

        self.y = self.end_y - self.start_y
        if self.y < 0:
            self.y = self.start_y - self.end_y


        self.steep = self.steepness()
        self.angle = self.angle()

        self.length = (self.x**2 + self.y**2) ** 0.5
        print(f"length :{self.length}")

        self.p1, self.p2 = p1, p2

    def steepness(self):
        x = self.end_x - self.start_x
        if x < 0:
            x = self.start_x - self.end_x

        y = self.end_y - self.start_y
        if y < 0:
            y = self.start_y - self.end_y

        return y/x

    def angle(self):
        theta_rad = math.atan(self.steep)  # angle in radians
        theta_deg = math.degrees(theta_rad)
        return theta_deg

    def draw_line(self, frame):

        cv2.line(frame, self.p1, self.p2, (255, 255, 0), 2)

def add_pixels(frame, add):
    top, bottom, left, right = add, add, add, add

    # Option 1: constant (black) border
    padded = cv2.copyMakeBorder(
        frame,
        top, bottom, left, right,
        borderType=cv2.BORDER_CONSTANT,
        value=[0, 0, 0]  # BGR color for the border
    )

    return padded


def big_crop(change:float, lines:dict[int, Line]):
    """
    l_ret = []

    for i, (x, y) in enumerate(pos):
        if i == 0:
            x -= change
            y -= change
        if i == 1:
            x += change
            y -= change
        if i == 2:
            x += change
            y += change
        if i == 3:
            x -= change
            y += change
        l_ret.append((x, y))
        """
    l_ret = []

    for i, line in lines.items():
        if i == 0:
            x = line.p1[0] - line.length * change
            y = line.p1[1] - lines[3].length * change
        if i == 1:
            x = line.p1[0] + lines[0].length * change
            y = line.p1[1] - line.length * change
        if i == 2:
            x = line.p1[0] + line.length * change
            y = line.p1[1] + lines[1].length * change
        if i == 3:
            x = line.p1[0] - lines[2].length * change
            y = line.p1[1] + line.length * change

        l_ret.append((round(x), round(y)))

    return l_ret


def point(x, y):
    global frame
    cv2.circle(frame, (round(x), round(y)), 5, (0, 0, 255), -1)


def add_to_pos(points, add):
    points_copy = []
    for x, y in points:
        points_copy.append((x + add, y + add))

    return points_copy



def resize(frame, mult):

    h, w = frame.shape[:2]

    smaller = cv2.resize(
        frame,
        (round(w*mult), round(h*mult)),
        interpolation=cv2.INTER_AREA
    )
    return smaller


def make_lines(points, add):
    d = {}

    for i, p1 in enumerate(points):
        if i + 1 < len(points):
            p2 = points[i + 1]
        else:
            p2 = points[0]

        d[i] = Line(p1, p2)

    #print(d)
    return d

def actual_pos(x, y, i=False):
    if i:
        x += zer_zero_pos[0]
        y -= max_max_pos[1]
        return x, y
    x -= zer_zero_pos[0]
    y += max_max_pos[1]
    return x, y



aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
parameters = cv2.aruco.DetectorParameters()

# Create the ArUco detector
detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)

pos = [(189, 215), (943, 178), (975, 803), (207, 829)]

zer_zero_pos = (137, 1038)
max_max_pos = (972, 79)

max_measured_pos = (836, 957)

x_pixel_move = max_max_pos[0] - zer_zero_pos[0]
y_pixel_move = zer_zero_pos[1] - max_max_pos[1]


mid_point = (max_max_pos[0] / 2, max_max_pos[1] / 2)


add = 200

pos = add_to_pos(pos, add)

mult = 0.4

lines = make_lines(pos, add)

big_pos = big_crop(mult, lines)


print(big_pos)


crop_lines = make_lines(big_pos, add)

crop_pos = []

for i, line in crop_lines.items():
    crop_pos.append(line.p1)


for _, line in lines.items():
    print(line.angle)

while True:


    ret, frame = cap.read()
    frame = add_pixels(frame, add)
    #cv2.imshow("org", frame)
    # cv2.imshow(str(random.randint(0, 100)), frame)
    if not ret:
        print("Error: Failed to capture frame: ERROR")
    else:
        pass

    frame = Img.warp_frame_to_rectangle(frame, crop_pos)


    frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    hx, hy, frame = get_hand_mark(frame, detector)

    if hx is None or hy is None:
        continue

    hy = Img.invert(hy, y_pixel_move)

    hx,hy = actual_pos(hx, hy)

    print(hx, hy)


    point(*actual_pos(*mid_point, i=True))

    frame = resize(frame, 0.8)

    cv2.imshow("mark", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
