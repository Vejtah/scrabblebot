import cv2
import pytesseract


import numpy as np
#from pipenv.pep508checker import implementation_name

try:
    from config import Constants
    import data
except ModuleNotFoundError:
    from functions.config import Constants

    from functions import data

# Optional: Set tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'  # on linux

def resize(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply threshold to isolate the letter (tweak as needed)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Resize to improve OCR accuracy (optional)
    resized = cv2.resize(thresh, (0, 0), fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
    
    return resized


def extract_letter(resized):
    # Convert to grayscale

    #cv2.imshow("prepared", resized)

    # OCR config: Single character mode with whitelist
    config = r'--psm 10 -c tessedit_char_whitelist=' + Constants.Image.available_letters

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

def get_black_pixel_percentage(gray, d=False, bw=None) -> float:
    
    # 3. Threshold to pure black | white
    #    You can pick a fixed threshold (e.g. 127) or use Otsu’s method to choose it automatically:
            
    if bw is None:
        _, bw = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)


    # 4. Compute percentage of black pixels
    total_pixels = bw.size
    black_pixels = np.count_nonzero(bw == 0)
    black_percent = (black_pixels / total_pixels) * 100
    
    if d:
        print(f'Black pixels: {black_pixels}/{total_pixels} ({black_percent:.2f}%)')
    return black_percent

def is_letter(black_val:float)->bool:
    mid_point = data.clac_midpoint(data.load(Constants.System.json_path_black_vals))
    
    if black_val < mid_point:
        return True
    return False
