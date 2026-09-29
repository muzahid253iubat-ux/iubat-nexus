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

# --- Custom CSS for Minimalist Card Layout ---
st.markdown(f"""
    <style>
    .stApp {{
        background: #E8F0F2;
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
    
    /* Soft overlay for clarity */
    .stApp::after {{
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(230, 240, 245, 0.75);
        z-index: 0;
    }}
    
    .block-container {{
        position: relative;
        z-index: 1;
        padding-top: 4rem !important;
        padding-bottom: 2rem !important;
        max-width: 440px !important;
    }}
    
    #MainMenu, header, footer {{visibility: hidden;}}
    
    /* Top Avatar Overlapping Card */
    .avatar-wrapper {{
        display: flex;
        justify-content: center;
        margin-bottom: -42px;
        position: relative;
        z-index: 10;
    }}
    
    .avatar-circle {{
        background: #0A192F;
        width: 84px;
        height: 84px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 10px 25px rgba(10, 25, 47, 0.25), 0 0 0 6px rgba(255, 255, 255, 0.9);
        border: 2px solid #FFFFFF;
        color: #FFFFFF;
        font-size: 38px;
    }}
    
    /* Main Card */
    .login-card {{
        background: #FFFFFF;
        border-radius: 24px;
        padding: 55px 32px 32px 32px;
        box-shadow: 0 20px 45px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.8);
    }}
    
    /* Form Styling */
    div[data-testid="stForm"] {{
        background: transparent !important;
        padding: 0px !important;
        border: none !important;
        box-shadow: none !important;
    }}
    
    div[data-testid="stForm"] label p {{
        display: none !important;
    }}
    
    .stTextInput>div>div>input {{
        background-color: #E9ECEF !important;
        color: #334155 !important;
        font-weight: 600;
        border-radius: 8px;
        border: none;
        padding: 12px 16px;
        font-size: 0.95rem;
    }}
    
    .stTextInput>div>div>input:focus {{
        background-color: #DEE2E6 !important;
        box-shadow: none;
        border: 1px solid #0A192F;
    }}
    
    /* Remember Me & Forgot Password Layout */
    .row-options {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 5px;
        margin-bottom: 15px;
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
        transition: color 0.2s;
    }}
    
    .forgot-pass:hover {{
        color: #0A192F;
        text-decoration: underline;
    }}
    
    /* Login Button */
    .stFormSubmitButton>button {{
        width: 100% !important;
        background: #0A192F !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        letter-spacing: 1.5px;
        border: none !important;
        padding: 13px !important;
        border-radius: 8px !important;
        box-shadow: 0 6px 15px rgba(10, 25, 47, 0.2) !important;
        margin-top: 5px !important;
        transition: all 0.3s ease !important;
    }}
    
    .stFormSubmitButton>button:hover {{
        background: #112240 !important;
        transform: translateY(-1px);
    }}
    
    .portal-footer {{
        text-align: center;
        color: #475569;
        font-size: 11px;
        margin-top: 25px;
        font-weight: 600;
        letter-spacing: 0.3px;
    }}
    </style>
""", unsafe_allow_html=True)

# --- UI Render ---

# Floating Avatar Header
st.markdown("""
    <div class='avatar-wrapper'>
        <div class='avatar-circle'>👤</div>
    </div>
""", unsafe_allow_html=True)

# Main Login Card Container
st.markdown("<div class='login-card'>", unsafe_allow_html=True)

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

st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("<div class='portal-footer'>IUBAT Nexus • Version 1.0.0 Beta<br>© 2026 All Rights Reserved</div>", unsafe_allow_html=True)
