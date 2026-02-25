import streamlit as st
import sqlite3
import pandas as pd
from assets.theme import apply_theme

apply_theme()
st.title("📜 Prediction History")

conn = sqlite3.connect("database/predictions.db", check_same_thread=False)

df = pd.read_sql(
    "SELECT image_name AS Image, prediction AS Prediction, time AS Time FROM history ORDER BY id DESC",
    conn
)

if df.empty:
    st.warning("No predictions yet.")
else:
    st.dataframe(df, use_container_width=True)