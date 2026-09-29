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

# --- Custom CSS for Clean Glassmorphism & High Readability ---
st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(10, 25, 47, 0.78), rgba(15, 23, 42, 0.85)), 
                    url('{bg_image_data}');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-repeat: no-repeat;
    }}
    
    .main-title {{
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #00C6FF 0%, #0072FF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        letter-spacing: 1px;
        margin-bottom: 0px;
        text-shadow: 0 4px 20px rgba(0, 198, 255, 0.3);
    }}
    
    .sub-title {{
        color: #CBD5E1 !important;
        text-align: center;
        font-size: 1.1rem;
        font-weight: 500;
        margin-top: 5px;
        margin-bottom: 30px;
        letter-spacing: 0.5px;
    }}
    
    .login-container {{
        background: rgba(255, 255, 255, 0.08);
        padding: 40px;
        border-radius: 24px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        max-width: 440px;
        margin: 0 auto;
    }}
    
    .login-header {{
        color: #FFFFFF !important;
        text-align: center;
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 25px;
        letter-spacing: 0.5px;
    }}
    
    label {{
        color: #F1F5F9 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }}
    
    .stTextInput>div>div>input {{
        background-color: rgba(15, 23, 42, 0.7) !important;
        color: #ffffff !important;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 14px;
        font-size: 1rem;
    }}
    
    .stTextInput>div>div>input:focus {{
        border-color: #00C6FF;
        box-shadow: 0 0 12px rgba(0, 198, 255, 0.4);
    }}
    
    .stButton>button {{
        width: 100%;
        background: linear-gradient(135deg, #00C6FF 0%, #0072FF 100%);
        color: white;
        font-weight: 700;
        font-size: 1.05rem;
        border: none;
        padding: 14px;
        border-radius: 12px;
        box-shadow: 0 6px 20px rgba(0, 114, 255, 0.4);
        transition: all 0.3s ease;
        margin-top: 10px;
    }}
    
    .stButton>button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 114, 255, 0.6);
    }}
    
    .footer {{
        text-align: center;
        color: rgba(255, 255, 255, 0.6);
        font-size: 12px;
        margin-top: 50px;
        letter-spacing: 0.5px;
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
