import cv2, time

class Image:
    def __init__(self):
        for idx in range(4):
            cap = cv2.VideoCapture(idx, cv2.CAP_V4L2)
            time.sleep(0.1)

            if not cap.isOpened():
                continue

            # do we actually get a frame?
            ret, frame = cap.read()
            cv2.imshow(str(idx), frame)
            time.sleep(3)
            if not ret or frame is None or frame.size == 0:
                cap.release()
                continue

            print(f"→ using camera index {idx}")
            self.cap = cap
            return

        raise SystemError("Error: Cannot access any usable camera")
Img = Image()
