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

# --- Custom CSS (Removed Blue Overlay, Clean Background & Fixed Inputs) ---
st.markdown(f"""
    <style>
    .stApp {{
        background: url('{bg_image_data}');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-repeat: no-repeat;
    }}
    
    #MainMenu, header, footer {{visibility: hidden;}}
    
    .block-container {{
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
        max-width: 460px !important;
    }}
    
    /* First Section: Banner Card */
    .banner-card {{
        background: rgba(15, 23, 42, 0.75);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        border-radius: 20px;
        padding: 35px 20px;
        text-align: center;
        color: white;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin-bottom: 24px;
    }}
    
    .banner-crest {{
        background: #0F172A;
        width: 54px;
        height: 54px;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
        border: 3px solid rgba(255, 255, 255, 0.9);
        font-size: 24px;
        margin-bottom: 10px;
    }}
    
    .banner-title {{
        font-size: 1.3rem;
        font-weight: 800;
        letter-spacing: 0.5px;
        text-shadow: 0 2px 6px rgba(0, 0, 0, 0.7);
    }}
    
    .banner-subtitle {{
        font-size: 0.68rem;
        color: #CBD5E1;
        margin-top: 4px;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
        text-shadow: 0 1px 4px rgba(0, 0, 0, 0.7);
    }}
    
    /* Second Section: Floating Login Card */
    .avatar-container {{
        display: flex;
        justify-content: center;
        margin-bottom: -36px;
        position: relative;
        z-index: 10;
    }}
    
    .avatar-circle {{
        background: #0F172A;
        width: 72px;
        height: 72px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.35), 0 0 0 5px rgba(255, 255, 255, 0.25);
        border: 3px solid #FFFFFF;
        font-size: 32px;
    }}
    
    .login-card {{
        background: #FFFFFF;
        border-radius: 24px;
        padding: 45px 28px 24px 28px;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }}
    
    /* Form Styling inside Login Card */
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
        background-color: #F8FAFC !important;
        color: #0F172A !important;
        font-weight: 600;
        border-radius: 10px;
        border: 1.5px solid #E2E8F0;
        padding: 11px 14px;
        font-size: 0.9rem;
        transition: all 0.3s ease;
    }}
    
    .stTextInput>div>div>input:focus {{
        background-color: #FFFFFF !important;
        border-color: #0F172A;
        box-shadow: 0 0 0 3px rgba(15, 23, 42, 0.1);
    }}
    
    .stCheckbox label p {{
        display: block !important;
        color: #475569 !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
    }}
    
    .stFormSubmitButton>button {{
        width: 100% !important;
        background: #0F172A !important;
        color: white !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        letter-spacing: 1px;
        border: none !important;
        padding: 12px !important;
        border-radius: 10px !important;
        box-shadow: 0 6px 18px rgba(15, 23, 42, 0.3) !important;
        margin-top: 10px !important;
        transition: all 0.3s ease !important;
    }}
    
    .stFormSubmitButton>button:hover {{
        background: #1E293B !important;
        box-shadow: 0 8px 22px rgba(15, 23, 42, 0.4) !important;
        transform: translateY(-1px);
    }}
    
    .portal-footer {{
        text-align: center;
        color: #E2E8F0;
        font-size: 11px;
        margin-top: 20px;
        font-weight: 600;
        letter-spacing: 0.3px;
        text-shadow: 0 1px 3px rgba(0, 0, 0, 0.8);
    }}
    </style>
""", unsafe_allow_html=True)

# --- UI Render ---

# 1st Section: Banner Card
st.markdown("""
    <div class='banner-card'>
        <div class='banner-crest'>🎓</div>
        <div class='banner-title'>IUBAT Nexus</div>
        <div class='banner-subtitle'>Excellence in Higher Education & Research</div>
    </div>
""", unsafe_allow_html=True)

# 2nd Section: Floating Login Card
st.markdown("""
    <div class='avatar-container'>
        <div class='avatar-circle'>👤</div>
    </div>
""", unsafe_allow_html=True)

st.markdown("<div class='login-card'>", unsafe_allow_html=True)

with st.form("login_form"):
    user_id = st.text_input("ID Number", placeholder="👤 ID Number")
    password = st.text_input("Password", type="password", placeholder="🔒 Password")

    remember_me = st.checkbox("Remember me")

    submit_btn = st.form_submit_button("LOGIN")
    if submit_btn:
        if user_id and password:
            st.success(f"Welcome back, {user_id}!")
        else:
            st.error("❌ Please enter both ID Number and Password.")

st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("<div class='portal-footer'>Version : 1.0.0 Beta<br>© 2026 IUBAT Nexus</div>", unsafe_allow_html=True)
