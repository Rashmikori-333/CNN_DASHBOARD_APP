import numpy as np
from tensorflow.keras.models import load_model
from utils.preprocess import preprocess_image

CLASS_NAMES = ["Cat", "Dog", "Fruit"]

model = load_model("model/mobilenet_cnn.h5")

def predict_image(img):
    processed = preprocess_image(img)
    preds = model.predict(processed)[0]
    index = np.argmax(preds)
    confidence = preds[index] * 100
    return CLASS_NAMES[index], round(confidence, 2)
