import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models

# 1) ImageDataGenerators
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=10,
    width_shift_range=0.1,
    height_shift_range=0.1,
    zoom_range=0.1,
    shear_range=0.1
)
val_datagen = ImageDataGenerator(rescale=1./255)

train_dir = "dataset/train"
val_dir   = "dataset/val"

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(64, 64),
    batch_size=32,
    class_mode='categorical'
)
val_generator = val_datagen.flow_from_directory(
    val_dir,
    target_size=(64, 64),
    batch_size=32,
    class_mode='categorical'
)

# 2) Define the model
num_classes = 26
model = models.Sequential([
    layers.Conv2D(32, (3,3), activation='relu', input_shape=(64, 64, 3)),
    layers.MaxPooling2D((2,2)),
    
    layers.Conv2D(64, (3,3), activation='relu'),
    layers.MaxPooling2D((2,2)),
    
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(num_classes, activation='softmax')
])

model.summary()

# 3) Compile the model
model.compile(
    loss='categorical_crossentropy',
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

test_image_path = "path_to_new_image.jpg"
img = cv2.imread(test_image_path)
img = cv2.resize(img, (64, 64))
img = img.astype('float32') / 255.0
img = np.expand_dims(img, axis=0)

pred = model.predict(img)  # shape: (1, 26)
predicted_idx = np.argmax(pred[0])

# Reverse lookup the class from the index
inv_map = {v: k for k, v in train_generator.class_indices.items()}
print("Predicted letter:", inv_map[predicted_idx])
