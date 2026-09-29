import streamlit as st
import os
import base64

# --- Configuration ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(SCRIPT_DIR, "assets")

def get_campus_images():
    images = []
    if os.path.exists(ASSETS_DIR):
        for filename in sorted(os.listdir(ASSETS_DIR)):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                images.append(os.path.join(ASSETS_DIR, filename))
    return images

# --- App Setup ---
st.set_page_config(
    page_title="IUBAT Nexus | Portal",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS for Slideshow & Glassmorphism ---
st.markdown("""
    <style>
    .slideshow-container {
        position: fixed;
        width: 100vw;
        height: 100vh;
        top: 0;
        left: 0;
        z-index: -1;
        overflow: hidden;
    }
    
    .slide {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-size: cover;
        background-position: center;
        opacity: 0;
        animation: fadeEffect 16s infinite;
    }
    
    @keyframes fadeEffect {
        0% { opacity: 0; }
        10% { opacity: 1; }
        33% { opacity: 1; }
        43% { opacity: 0; }
        100% { opacity: 0; }
    }
    
    /* Dynamically assign delays based on slide index injected via code */
    
    .login-container {
        background: rgba(15, 23, 42, 0.75);
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.6);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        margin-top: 8vh;
        max-width: 450px;
        margin-left: auto;
        margin-right: auto;
    }
    
    h1, h2, h3, p, label {
        color: #ffffff !important;
        text-align: center;
        font-family: 'Inter', sans-serif;
    }
    
    .stTextInput>div>div>input {
        background-color: rgba(255, 255, 255, 0.1);
        color: white;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #FF4B2B 0%, #FF416C 100%);
        color: white;
        font-weight: bold;
        border: none;
        padding: 12px;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(255, 75, 43, 0.4);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 75, 43, 0.6);
    }
    
    .footer {
        position: fixed;
        left: 0;
        bottom: 15px;
        width: 100%;
        text-align: center;
        color: rgba(255, 255, 255, 0.6);
        font-size: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Dynamic Background Render ---
campus_images = get_campus_images()

if campus_images:
    slides_html = ""
    total_images = len(campus_images)
    duration_per_image = 16 / total_images if total_images > 0 else 16
    
    for idx, img_path in enumerate(campus_images):
        with open(img_path, "rb") as img_file:
            encoded_string = base64.b64encode(img_file.read()).decode()
            mime_type = "image/jpeg" if img_path.lower().endswith(('.jpg', '.jpeg')) else "image/png"
            img_src = f"data:{mime_type};base64,{encoded_string}"
            
            delay = idx * duration_per_image
            slides_html += f"<div class='slide' style='background-image: url(\"{img_src}\"); animation-delay: {delay}s;'></div>\n"
            
    st.markdown(f"<div class='slideshow-container'>{slides_html}</div>", unsafe_allow_html=True)
else:
    st.warning("⚠️ No images found inside 'assets' folder in GitHub!")

# --- Main Login UI ---
st.markdown("<h1>🎓 IUBAT Nexus</h1>", unsafe_allow_html=True)
st.markdown("<p>Your Smart University Companion Portal</p>", unsafe_allow_html=True)
st.write("")

with st.container():
    st.markdown("<div class='login-container'>", unsafe_allow_html=True)
    st.markdown("<h3>Portal Sign In</h3>", unsafe_allow_html=True)
    
    user_id = st.text_input("Student ID / Email", placeholder="e.g., 20103056")
    password = st.text_input("Password", type="password", placeholder="••••••••")
    
    st.write("")
    if st.button("Secure Login"):
        if user_id and password:
            st.success(f"Welcome back, {user_id}!")
        else:
            st.error("❌ Please enter both ID and password.")
            
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='footer'>Developed by Muzahid | IUBAT Nexus Beta © 2026</div>", unsafe_allow_html=True)
