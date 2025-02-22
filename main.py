import cv2
import pytesseract

# Set the path to Tesseract-OCR executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def capture_and_extract_text():
    # Initialize camera
    cap = cv2.VideoCapture(1)  # 0 for default camera

    while True:
        # Read frame from the camera
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break

        # Display the live camera feed
        cv2.imshow("Camera Feed", frame)

        # Wait for the user to press 's' to take a snapshot or 'q' to quit
        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):  # Press 's' to capture
            # Convert the image to grayscale (optional, for better OCR performance)
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray_frame_n = cv2.threshold(gray_frame, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

            
            # Extract text from the image using pytesseract
            extracted_text = pytesseract.image_to_string(gray_frame_n)
            print("Extracted Text:")
            print(extracted_text)
            make_txt_usable(extracted_text)
             # stop the loop

        elif key == ord('q'):  # Press 'q' to quit
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()


def make_txt_usable(raw_txt):#
    
    print(f"looped: {raw_txt}")


# Run the function

capture_and_extract_text()

