import streamlit as st
import os
import base64

# --- App Setup ---
st.set_page_config(
    page_title="IUBAT Nexus | Portal",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Dynamic Assets Image Reader for Slideshow ---
assets_dir = os.path.join(os.getcwd(), "assets")

def get_all_campus_images():
    images = []
    if os.path.exists(assets_dir):
        for filename in sorted(os.listdir(assets_dir)):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                img_path = os.path.join(assets_dir, filename)
                with open(img_path, "rb") as f:
                    encoded = base64.b64encode(f.read()).decode()
                    mime = "image/jpeg" if filename.lower().endswith(('.jpg', '.jpeg')) else "image/png"
                    images.append(f"data:{mime};base64,{encoded}")
    return images

campus_images = get_all_campus_images()

# Fallback if no images found
if not campus_images:
    campus_images = ["https://images.unsplash.com/photo-1541339907198-e08756dedf3f?auto=format&fit=crop&w=1950&q=80"]

total_images = len(campus_images)
animation_duration = total_images * 5  # 5 seconds per image

# Generate slide divs dynamically
slides_html = ""
for idx, img_data in enumerate(campus_images):
    delay = idx * 5
    slides_html += f"""
    <div class="slide" style="background-image: linear-gradient(rgba(10, 25, 47, 0.75), rgba(10, 25, 47, 0.82)), url('{img_data}'); animation-delay: {delay}s; animation-duration: {animation_duration}s;"></div>
    """

# --- Custom CSS for Smooth Slideshow & Glassmorphism ---
st.markdown(f"""
    <style>
    .slideshow-container {{
        position: fixed;
        width: 100vw;
        height: 100vh;
        top: 0;
        left: 0;
        z-index: -999;
        overflow: hidden;
    }}
    
    .slide {{
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-size: cover;
        background-position: center;
        opacity: 0;
        animation-name: fadeSlide;
        animation-iteration-count: infinite;
        animation-timing-function: ease-in-out;
    }}
    
    @keyframes fadeSlide {{
        0% {{ opacity: 0; }}
        10% {{ opacity: 1; }}
        30% {{ opacity: 1; }}
        40% {{ opacity: 0; }}
        100% {{ opacity: 0; }}
    }}
    
    .login-container {{
        background: rgba(255, 255, 255, 0.08);
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        margin-top: 50px;
        max-width: 450px;
        margin-left: auto;
        margin-right: auto;
    }}
    
    h1, h2, h3, p, label {{
        color: #ffffff !important;
        text-align: center;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}
    
    .stTextInput>div>div>input {{
        background-color: rgba(255, 255, 255, 0.15);
        color: white;
        border-radius: 10px;
        border: none;
        padding: 12px;
    }}
    
    .stButton>button {{
        width: 100%;
        background: linear-gradient(135deg, #FF4B2B 0%, #FF416C 100%);
        color: white;
        font-weight: bold;
        border: none;
        padding: 12px;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(255, 75, 43, 0.4);
        transition: all 0.3s ease;
    }}
    .stButton>button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 75, 43, 0.6);
    }}
    
    .footer {{
        position: fixed;
        left: 0;
        bottom: 20px;
        width: 100%;
        text-align: center;
        color: rgba(255, 255, 255, 0.5);
        font-size: 12px;
    }}
    </style>
    
    <div class="slideshow-container">
        {slides_html}
    </div>
""", unsafe_allow_html=True)

# --- Main App Content ---
st.markdown("<h1>🎓 IUBAT Nexus</h1>", unsafe_allow_html=True)
st.markdown("<p>Your Smart University Companion Portal</p>", unsafe_allow_html=True)
st.write("")

with st.container():
    st.markdown("<div class='login-container'>", unsafe_allow_html=True)
    st.markdown("<h3>Sign In</h3>", unsafe_allow_html=True)
    
    user_id = st.text_input("Student ID", placeholder="e.g. 20103056")
    password = st.text_input("Password", type="password", placeholder="••••••••")
    
    st.write("")
    if st.button("Submit Login"):
        if user_id and password:
            st.success(f"Welcome back, {user_id}!")
        else:
            st.error("❌ Please enter both Student ID and Password.")
            
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='footer'>Developed by Muzahid | IUBAT Nexus Beta © 2026</div>", unsafe_allow_html=True)
