import numpy as np
import cv2
import os
import json
import keras
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models

with open("class_indices.json", "r") as f:
    class_indices = json.load(f)

inv_map = {v: k for k, v in class_indices.items()}
print(inv_map)

cap = cv2.VideoCapture(1) 
model = load_model("C:/Users/vit/myenv/pen_headphones.keras")

def predict(img):
    


    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    img = cv2.resize(img, (64, 64))
    img = img.astype('float32') / 255.0
    img = np.expand_dims(img, axis=0)

    pred = model.predict(img)  # pred has shape (1, 1)
    predicted_class = 1 if pred[0][0] >= 0.5 else 0
    print(predicted_class)
    print("Predicted value:", pred[0][0])
    print("Predicted class index:", predicted_class)

    #Reverse lookup the class from the index
    print("Mapping:", inv_map)


    predicted = inv_map[predicted_class]
    return predicted

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to read from camera.")
        predict(frame)
    
    cv2.imshow("Live Feed", frame)
    
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord(' '):
        predicted = predict(frame)
        print(predicted)
        

    elif key == ord('q'):
        print("Exiting...")
        break

cap.release()
cv2.destroyAllWindows()
