import streamlit as st
from assets.theme import apply_theme

apply_theme()

st.title("📊 CNN Dashboard App")
st.subheader("Image Classification Dashboard")

st.markdown("""
<div class="glass-card">
Use the sidebar to:
• Upload images  
• View prediction history  
• Explore analytics  
</div>
""", unsafe_allow_html=True)
