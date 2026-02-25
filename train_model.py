import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from sklearn.metrics import confusion_matrix, classification_report
import numpy as np
import os

# ---------------- BASIC SETTINGS ----------------
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 15

# ---------------- DATA AUGMENTATION ----------------
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=30,
    width_shift_range=0.2,
    height_shift_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    brightness_range=[0.7, 1.3],
    fill_mode="nearest"
)

train_data = train_datagen.flow_from_directory(
    "../dataset/train",
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    shuffle=False   # IMPORTANT for evaluation
)

print("📂 Classes:", train_data.class_indices)

# ---------------- CNN MODEL ----------------
model = Sequential([
    Conv2D(32, (3,3), activation="relu", input_shape=(224,224,3)),
    MaxPooling2D(2,2),

    Conv2D(64, (3,3), activation="relu"),
    MaxPooling2D(2,2),

    Flatten(),
    Dense(128, activation="relu"),
    Dense(3, activation="softmax")   # Cat, Dog, Fruit
])

model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

# ---------------- TRAINING ----------------
history = model.fit(
    train_data,
    epochs=EPOCHS
)

# ---------------- EVALUATION (TRAIN DATA) ----------------
y_pred = model.predict(train_data)
y_pred_classes = np.argmax(y_pred, axis=1)
y_true = train_data.classes

# Confusion Matrix
cm = confusion_matrix(y_true, y_pred_classes)
print("\n📊 Confusion Matrix:\n", cm)

# Classification Report
print("\n📄 Classification Report:\n")
print(classification_report(
    y_true,
    y_pred_classes,
    target_names=list(train_data.class_indices.keys())
))

# ---------------- SAVE MODEL ----------------
MODEL_PATH = "../model/cnn_model.keras"
model.save(MODEL_PATH)
print(f"\n✅ Model trained & saved successfully at {MODEL_PATH}")