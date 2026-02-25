import streamlit as st
import sqlite3
import pandas as pd
import altair as alt
from assets.theme import apply_theme

# ---------------- APPLY THEME ----------------
apply_theme()

st.title("📊 Analytics Dashboard")
st.caption("Visual insights from image predictions")

# ---------------- DATABASE ----------------
try:
    conn = sqlite3.connect("database/predictions.db", check_same_thread=False)
    df = pd.read_sql("SELECT * FROM history", conn)
except Exception as e:
    st.error("❌ Database not found or table missing")
    st.stop()

# ---------------- DATA SAFETY ----------------
if df.empty:
    st.warning("No analytics data available yet.")
    st.stop()

# Standardize prediction labels
df["prediction"] = df["prediction"].astype(str).str.capitalize()

# Keep only valid classes
df = df[df["prediction"].isin(["Cat", "Dog", "Fruit"])]

if df.empty:
    st.warning("No valid prediction data found.")
    st.stop()

# Convert time safely
df["time"] = pd.to_datetime(df["time"], errors="coerce")
df = df.dropna(subset=["time"])

# ---------------- FILTER ----------------
st.markdown("### 🔍 Filter Predictions")

selected = st.multiselect(
    "Select Classes",
    options=["Cat", "Dog", "Fruit"],
    default=["Cat", "Dog", "Fruit"]
)

df = df[df["prediction"].isin(selected)]

if df.empty:
    st.warning("No data after applying filter.")
    st.stop()

# ---------------- METRICS ----------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="glass-card">
        <h3>📦 Total Predictions</h3>
        <h1>{len(df)}</h1>
    </div>
    """, unsafe_allow_html=True)

with col2:
    top_label = df["prediction"].value_counts().idxmax()
    st.markdown(f"""
    <div class="glass-card">
        <h3>🏆 Top Prediction</h3>
        <h1>{top_label}</h1>
    </div>
    """, unsafe_allow_html=True)

with col3:
    today_count = df[df["time"].dt.date == pd.Timestamp.now().date()]
    st.markdown(f"""
    <div class="glass-card">
        <h3>📅 Today</h3>
        <h1>{len(today_count)}</h1>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ---------------- DONUT CHART ----------------
st.markdown("### 🍩 Prediction Distribution")

donut = alt.Chart(df).mark_arc(innerRadius=70).encode(
    theta=alt.Theta("count():Q"),
    color=alt.Color("prediction:N", legend=alt.Legend(title="Class")),
    tooltip=["prediction:N", "count():Q"]
)

st.altair_chart(donut, use_container_width=True)

# ---------------- BAR CHART ----------------
st.markdown("### 📊 Class Frequency")

bar = alt.Chart(df).mark_bar(
    cornerRadiusTopLeft=10,
    cornerRadiusTopRight=10
).encode(
    x=alt.X("prediction:N", title="Class"),
    y=alt.Y("count():Q", title="Count"),
    color="prediction:N",
    tooltip=["prediction:N", "count():Q"]
)

st.altair_chart(bar, use_container_width=True)

# ---------------- TIMELINE ----------------
st.markdown("### ⏳ Activity Over Time")

timeline_df = df.groupby(df["time"].dt.date).size().reset_index(name="count")

line = alt.Chart(timeline_df).mark_line(point=True).encode(
    x=alt.X("time:T", title="Date"),
    y=alt.Y("count:Q", title="Predictions"),
    tooltip=["time:T", "count:Q"]
)

st.altair_chart(line, use_container_width=True)

# ---------------- FOOTER ----------------
st.markdown("""
<div class="glass-card" style="text-align:center">
✨ Analytics powered by CNN Dashboard App
</div>
""", unsafe_allow_html=True)
