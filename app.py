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

# --- Custom CSS ---
st.markdown(f"""
    <style>
    .stApp {{
        background: #0F172A;
    }}
    
    /* Subtle Light Blur Background (3px) */
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: url('{bg_image_data}') no-repeat center center fixed;
        background-size: cover;
        filter: blur(3px);
        -webkit-filter: blur(3px);
        transform: scale(1.05);
        z-index: 0;
    }}
    
    /* Darker overlay for high contrast readability */
    .stApp::after {{
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(15, 23, 42, 0.55);
        z-index: 0;
    }}
    
    .block-container {{
        position: relative;
        z-index: 1;
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
        max-width: 440px !important;
    }}
    
    #MainMenu, header, footer {{visibility: hidden;}}

    /* First Section: Crisp High-Contrast Banner Card */
    .banner-card {{
        background: linear-gradient(135deg, #090D16 0%, #1E293B 100%) !important;
        border-radius: 20px;
        padding: 30px 20px;
        text-align: center;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
        border: 1.5px solid rgba(255, 255, 255, 0.25);
        margin-bottom: 24px;
    }}
    
    .banner-crest {{
        background: #0A192F;
        width: 56px;
        height: 56px;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.5);
        border: 2.5px solid #FFFFFF;
        font-size: 24px;
        margin-bottom: 10px;
    }}
    
    .banner-title {{
        color: #FFFFFF !important;
        font-size: 1.35rem;
        font-weight: 800;
        letter-spacing: 0.5px;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.6);
    }}
    
    .banner-subtitle {{
        color: #38BDF8 !important;
        font-size: 0.7rem;
        margin-top: 5px;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        font-weight: 700;
        text-shadow: 0 1px 3px rgba(0, 0, 0, 0.6);
    }}

    /* Floating Avatar Header */
    .avatar-container {{
        display: flex;
        justify-content: center;
        margin-bottom: -45px;
        position: relative;
        z-index: 10;
    }}
    
    .avatar-circle {{
        background: #0A192F;
        width: 86px;
        height: 86px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3), 0 0 0 6px rgba(255, 255, 255, 0.95);
        border: 2px solid #FFFFFF;
        color: #FFFFFF;
        font-size: 38px;
    }}

    /* Form Container acting as White Card */
    div[data-testid="stForm"] {{
        background: #FFFFFF !important;
        border-radius: 24px !important;
        padding: 55px 32px 32px 32px !important;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3) !important;
        border: 1px solid rgba(255, 255, 255, 0.9) !important;
    }}
    
    div[data-testid="stForm"] label p {{
        display: none !important;
    }}
    
    .stTextInput>div>div>input {{
        background-color: #F1F5F9 !important;
        color: #1E293B !important;
        font-weight: 600;
        border-radius: 10px;
        border: 1.5px solid #E2E8F0;
        padding: 12px 16px;
        font-size: 0.95rem;
    }}
    
    .stTextInput>div>div>input:focus {{
        background-color: #FFFFFF !important;
        border-color: #0A192F;
        box-shadow: 0 0 0 3px rgba(10, 25, 47, 0.1);
    }}
    
    .stCheckbox label p {{
        display: block !important;
        color: #64748B !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
    }}
    
    .forgot-pass {{
        color: #64748B;
        font-size: 0.85rem;
        font-weight: 500;
        text-decoration: none;
    }}
    
    .forgot-pass:hover {{
        color: #0A192F;
        text-decoration: underline;
    }}
    
    .stFormSubmitButton>button {{
        width: 100% !important;
        background: #0A192F !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        letter-spacing: 1.5px;
        border: none !important;
        padding: 13px !important;
        border-radius: 10px !important;
        box-shadow: 0 8px 20px rgba(10, 25, 47, 0.25) !important;
        margin-top: 10px !important;
        transition: all 0.3s ease !important;
    }}
    
    .stFormSubmitButton>button:hover {{
        background: #112240 !important;
        transform: translateY(-1px);
    }}
    
    .portal-footer {{
        text-align: center;
        color: #FFFFFF;
        font-size: 11px;
        margin-top: 25px;
        font-weight: 600;
        letter-spacing: 0.3px;
        text-shadow: 0 1px 3px rgba(0, 0, 0, 0.8);
    }}
    </style>
""", unsafe_allow_html=True)

# --- UI Render ---

# 1st Section: Crisp Banner Card
st.markdown("""
    <div class='banner-card'>
        <div class='banner-crest'>🎓</div>
        <div class='banner-title'>IUBAT Nexus</div>
        <div class='banner-subtitle'>Smart Portal for Innovation & Academics</div>
    </div>
""", unsafe_allow_html=True)

# Floating Avatar Header
st.markdown("""
    <div class='avatar-container'>
        <div class='avatar-circle'>👤</div>
    </div>
""", unsafe_allow_html=True)

# Login Form (White Card)
with st.form("login_form"):
    user_id = st.text_input("Username", placeholder="👤 Username")
    password = st.text_input("Password", type="password", placeholder="🔒 Password")

    col1, col2 = st.columns([1.2, 1])
    with col1:
        remember_me = st.checkbox("Remember me")
    with col2:
        st.markdown("<div style='text-align: right; padding-top: 4px;'><a href='#' class='forgot-pass'>Forgot Password?</a></div>", unsafe_allow_html=True)

    submit_btn = st.form_submit_button("LOGIN")
    if submit_btn:
        if user_id and password:
            st.success(f"Welcome back, {user_id}!")
        else:
            st.error("❌ Please enter both Username and Password.")

# Footer
st.markdown("<div class='portal-footer'>IUBAT Nexus • Version 1.0.0 Beta<br>© 2026 All Rights Reserved</div>", unsafe_allow_html=True)
