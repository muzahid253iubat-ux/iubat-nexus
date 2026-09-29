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

# --- Dynamic Assets Image Reader ---
def get_local_image_as_base64(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            data = f.read()
            return base64.b64encode(data).decode()
    return None

# Scan assets folder dynamically
assets_dir = os.path.join(os.getcwd(), "assets")
background_css = ""

if os.path.exists(assets_dir):
    image_files = [f for f in os.listdir(assets_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
    if image_files:
        # Takes the first image dynamically found in the assets folder
        latest_image_path = os.path.join(assets_dir, image_files[0])
        encoded_img = get_local_image_as_base64(latest_image_path)
        if encoded_img:
            background_css = f"data:image/jpeg;base64,{encoded_img}"

# Fallback default if no image is found
if not background_css:
    background_css = "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?auto=format&fit=crop&w=1950&q=80"

# --- Custom CSS ---
st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(10, 25, 47, 0.78), rgba(10, 25, 47, 0.85)), 
                    url('{background_css}');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-repeat: no-repeat;
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
