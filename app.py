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

# --- Fixed Background Image Reader (Clean & Safe) ---
def get_fixed_background():
    assets_dir = os.path.join(os.getcwd(), "assets")
    
    # Check for exact 'bg.jpg' first
    target_path = os.path.join(assets_dir, "bg.jpg")
    
    # If bg.jpg doesn't exist, search for any clean image filename without weird spaces
    if not os.path.exists(target_path) and os.path.exists(assets_dir):
        for f in sorted(os.listdir(assets_dir)):
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')) and ' ' not in f:
                target_path = os.path.join(assets_dir, f)
                break
                
    # If still not found, grab the first available image
    if not os.path.exists(target_path) and os.path.exists(assets_dir):
        for f in sorted(os.listdir(assets_dir)):
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                target_path = os.path.join(assets_dir, f)
                break
                
    if os.path.exists(target_path):
        with open(target_path, "rb") as file:
            encoded = base64.b64encode(file.read()).decode()
            mime = "image/jpeg" if target_path.lower().endswith(('.jpg', '.jpeg')) else "image/png"
            return f"data:{mime};base64,{encoded}"
            
    # Fallback default high-res campus image if nothing found
    return "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?auto=format&fit=crop&w=1950&q=80"

bg_image_data = get_fixed_background()

# --- Custom CSS for Fixed Background & Glassmorphism ---
st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(10, 25, 47, 0.78), rgba(10, 25, 47, 0.85)), 
                    url('{bg_image_data}');
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

st.markdown("<div style='text-align: center; color: rgba(255,255,255,0.5); font-size: 12px; margin-top: 40px;'>Developed by Muzahid | IUBAT Nexus Beta © 2026</div>", unsafe_allow_html=True)
