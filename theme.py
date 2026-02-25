import streamlit as st

def apply_theme():
    st.markdown("""
    <style>
    .stApp {
        background:
        linear-gradient(rgba(5,10,20,0.85), rgba(5,10,20,0.85)),
        url("https://images.unsplash.com/photo-1518770660439-4636190af475");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #EAEAEA;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg,#0f2027,#203a43,#2c5364);
    }

    h1,h2,h3 {
        color: #00E5FF;
    }

    .stButton>button {
        background: linear-gradient(135deg,#00E5FF,#2979FF);
        color: black;
        border-radius: 12px;
        font-weight: bold;
    }

    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)
