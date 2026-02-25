import streamlit as st
import numpy as np
import sqlite3
from datetime import datetime
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from PIL import Image
from assets.theme import apply_theme

# Theme
apply_theme()

st.title("📤 Upload Image & Predict")
# load model
model = load_model("model/cnn_model.keras")

class_names = ["cat", "dog", "fruit"]

uploaded_file = st.file_uploader(
    "Upload an image (Cat / Dog / Fruit)",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    # --- Image show (controlled size) ---
    img = Image.open(uploaded_file).convert("RGB")
    img = img.resize((224, 224))
    st.image(img, caption="Uploaded Image", width=300)

    # --- Preprocessing ---
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # --- Prediction ---
    prediction = model.predict(img_array)
    predicted_class = class_names[np.argmax(prediction)]
    confidence = float(np.max(prediction) * 100)

    # --- Show result ---
    st.markdown("### 🧠 Prediction Result")
    st.success(f"Prediction: **{predicted_class.upper()}**")
    st.info(f"Confidence: **{confidence:.2f}%**")

    # --- Save to DB ---
    conn = sqlite3.connect("database/predictions.db", check_same_thread=False)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO history (image_name, prediction, time) VALUES (?, ?, ?)",
        (
            uploaded_file.name,
            predicted_class.upper(),
            datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        )
    )

    conn.commit()
    conn.close()