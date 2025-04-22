import cv2
import pytesseract
import numpy as np

from constans import Constants
from make_black_values import Data

Cons = Constants()
Dta = Data()

class SHIT:
    def __init__(self):
        pass

    # Optional: Set tesseract executable path
    # pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

    def resize(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Apply threshold to isolate the letter (tweak as needed)
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Resize to improve OCR accuracy (optional)
        resized = cv2.resize(thresh, (0, 0), fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
        return resized


    def extract_letter(self, resized, black_val):
        # Convert to grayscale

        #cv2.imshow("prepared", resized)

        # OCR config: Single character mode with whitelist
        config = r'--psm 10 -c tessedit_char_whitelist=' + Cons.Image.available_letters

        # Run OCR
        result = pytesseract.image_to_string(resized, config=config)

        # Clean and return result
        result = result.strip().upper()

        #print(f"mid_point: {mid_point}")
        #print(f"black_val: {black_val}")

        if len(result) == 1 and result.isalpha():
            # compare the dark pixel prc to the data

            return result

        return None  # in some cases the black % may not work

    def get_black_pixel_percentage(self, gray, gray_scale=True, threshold=30) -> float:
        # Convert to grayscale if not already
        if not gray_scale:
            gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
        #

        # Create a binary mask where black pixels are 1 (below threshold)
        black_mask = gray < threshold

        # Count black pixels and total pixels
        black_pixels = np.sum(black_mask)
        total_pixels = gray.shape[0] * gray.shape[1]

        # Calculate percentage
        percentage = (black_pixels / total_pixels) * 100
        return percentage

    def is_letter(self, black_val:float)->bool:
        if black_val < Dta.clac_midpoint(Dta.load()):
            return True
        return False
