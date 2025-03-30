import json
import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models



train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=10,
    width_shift_range=0.1,
    height_shift_range=0.1,
    zoom_range=0.1,
    shear_range=0.1
)
val_datagen = ImageDataGenerator(rescale=1./255)

train_dir = "C:/Users/vit/myenv/code/dataset/train"
val_dir   = "C:/Users/vit/myenv/code/dataset/val"

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(64, 64),
    batch_size=32,
    class_mode='binary'
)
val_generator = val_datagen.flow_from_directory(
    val_dir,
    target_size=(64, 64),
    batch_size=32,
    class_mode='binary'
)

# 2) Define the model
num_classes = 1
model = models.Sequential([
    layers.Conv2D(32, (3,3), activation='relu', input_shape=(64, 64, 3)),
    layers.MaxPooling2D((2,2)),
    
    layers.Conv2D(64, (3,3), activation='relu'),
    layers.MaxPooling2D((2,2)),
    
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(1, activation='sigmoid')
])

model.summary()

# 3) Compile the model
model.compile(
    loss='binary_crossentropy',
    optimizer='adam',
    metrics=['accuracy']
)

# 4) Train
EPOCHS = 10
history = model.fit(
    train_generator,
    epochs=EPOCHS,
    validation_data=val_generator
)

# 5) Evaluate
val_loss, val_acc = model.evaluate(val_generator, verbose=0)
print(f"Validation loss: {val_loss:.4f}")
print(f"Validation accuracy: {val_acc:.4f}")

# 6) Predict on a single image
# (make sure you have an image to test this with)
import cv2

test_image_path = "C:/Users/vit/myenv/code/dataset/check/check_1.jpg"
img = cv2.imread(test_image_path)

# VERY IMPOTRTANT else the model will not understand provided image!!!
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

img = cv2.resize(img, (64, 64))
img = img.astype('float32') / 255.0
img = np.expand_dims(img, axis=0)


pred = model.predict(img)  # pred has shape (1, 1)
predicted_class = 1 if pred[0][0] >= 0.5 else 0
print("Predicted value:", pred[0][0])
print("Predicted class index:", predicted_class)

#Reverse lookup the class from the index
inv_map = {v: k for k, v in train_generator.class_indices.items()}
print("Mapping:", inv_map)

for _ in range(5):
    print("")

print("Predicted label:", inv_map[predicted_class])

for _ in range(5):
    print("")

#save

model.save("pen_headphones.keras")
# Assuming train_generator.class_indices exists after training:
with open("class_indices.json", "w") as f:
    json.dump(train_generator.class_indices, f)


