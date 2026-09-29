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

# --- Fixed Background Image Reader ---
def get_fixed_background():
    assets_dir = os.path.join(os.getcwd(), "assets")
    target_path = os.path.join(assets_dir, "bg.jpg")
    
    if not os.path.exists(target_path) and os.path.exists(assets_dir):
        for f in sorted(os.listdir(assets_dir)):
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')) and ' ' not in f:
                target_path = os.path.join(assets_dir, f)
                break
                
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
            
    return "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?auto=format&fit=crop&w=1950&q=80"

bg_image_data = get_fixed_background()

# --- Custom CSS for Clear Background & Vibrant Unique Text Colors ---
st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0, 0, 0, 0.35), rgba(0, 0, 0, 0.5)), 
                    url('{bg_image_data}');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-repeat: no-repeat;
    }}
    
    .main-title {{
        font-size: 3rem;
        font-weight: 900;
        color: #FFD700;
        text-align: center;
        letter-spacing: 1.5px;
        margin-bottom: 0px;
        text-shadow: 0 3px 15px rgba(0, 0, 0, 0.8), 0 0 25px rgba(255, 215, 0, 0.4);
    }}
    
    .sub-title {{
        color: #00FFFF !important;
        text-align: center;
        font-size: 1.15rem;
        font-weight: 600;
        margin-top: 8px;
        margin-bottom: 35px;
        letter-spacing: 0.8px;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.9);
    }}
    
    .login-container {{
        background: rgba(10, 20, 35, 0.82);
        padding: 40px;
        border-radius: 24px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.7);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border: 1px solid rgba(255, 215, 0, 0.3);
        max-width: 440px;
        margin: 0 auto;
    }}
    
    .login-header {{
        color: #FFD700 !important;
        text-align: center;
        font-size: 1.9rem;
        font-weight: 800;
        margin-bottom: 25px;
        letter-spacing: 0.5px;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.6);
    }}
    
    label {{
        color: #00FFFF !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        text-shadow: 0 1px 5px rgba(0, 0, 0, 0.8);
    }}
    
    .stTextInput>div>div>input {{
        background-color: rgba(255, 255, 255, 0.95) !important;
        color: #0F172A !important;
        font-weight: 600;
        border-radius: 12px;
        border: 2px solid #00FFFF;
        padding: 14px;
        font-size: 1rem;
    }}
    
    .stTextInput>div>div>input:focus {{
        border-color: #FFD700;
        box-shadow: 0 0 15px rgba(255, 215, 0, 0.6);
    }}
    
    .stButton>button {{
        width: 100%;
        background: linear-gradient(135deg, #FFD700 0%, #FF8C00 100%);
        color: #0F172A;
        font-weight: 800;
        font-size: 1.1rem;
        border: none;
        padding: 14px;
        border-radius: 12px;
        box-shadow: 0 6px 20px rgba(255, 140, 0, 0.5);
        transition: all 0.3s ease;
        margin-top: 10px;
    }}
    
    .stButton>button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(255, 215, 0, 0.8);
        background: linear-gradient(135deg, #FFE135 0%, #FFA500 100%);
    }}
    
    .footer {{
        text-align: center;
        color: #FFFFFF;
        font-weight: 600;
        font-size: 13px;
        margin-top: 50px;
        letter-spacing: 0.5px;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.9);
    }}
    </style>
""", unsafe_allow_html=True)

# --- Main App Content ---
st.markdown("<div class='main-title'>🎓 IUBAT Nexus</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Your Smart University Companion Portal</div>", unsafe_allow_html=True)

with st.container():
    st.markdown("<div class='login-container'>", unsafe_allow_html=True)
    st.markdown("<div class='login-header'>Sign In</div>", unsafe_allow_html=True)
    
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
