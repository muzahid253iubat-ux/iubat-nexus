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

# --- Asset Readers (Background & Logo) ---
def get_asset_base64(filename):
    assets_dir = os.path.join(os.getcwd(), "assets")
    target_path = os.path.join(assets_dir, filename)
    
    if not os.path.exists(target_path) and os.path.exists(assets_dir):
        exts = ('.png', '.jpg', '.jpeg', '.webp')
        for f in sorted(os.listdir(assets_dir)):
            if f.lower().endswith(exts) and (filename.split('.')[0] in f.lower()):
                target_path = os.path.join(assets_dir, f)
                break
                
    if os.path.exists(target_path):
        with open(target_path, "rb") as file:
            encoded = base64.b64encode(file.read()).decode()
            mime = "image/jpeg" if target_path.lower().endswith(('.jpg', '.jpeg')) else "image/png"
            return f"data:{mime};base64,{encoded}"
    return None

def get_fixed_background():
    bg_data = get_asset_base64("bp.jpg")
    if bg_data:
        return bg_data
        
    assets_dir = os.path.join(os.getcwd(), "assets")
    if os.path.exists(assets_dir):
        exts = ('.png', '.jpg', '.jpeg', '.webp')
        for f in sorted(os.listdir(assets_dir)):
            if f.lower().endswith(exts):
                path = os.path.join(assets_dir, f)
                with open(path, "rb") as file:
                    encoded = base64.b64encode(file.read()).decode()
                    mime = "image/jpeg" if path.lower().endswith(('.jpg', '.jpeg')) else "image/png"
                    return f"data:{mime};base64,{encoded}"
                    
    return "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?auto=format&fit=crop&w=1950&q=80"

bg_image_data = get_fixed_background()
logo_image_data = get_asset_base64("logo.png")

# --- Custom CSS for IUBAT Campus Background ---
st.markdown(f"""
    <style>
    .stApp {{
        background: #090D16;
        display: flex;
        align-items: center;
        justify-content: center;
    }}
    
    /* IUBAT Campus Background Image with Perfect Full Fit */
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: url('{bg_image_data}') no-repeat center center fixed;
        background-size: cover;
        z-index: 0;
    }}
    
    /* Soft Dark Overlay for Crystal Clear Visibility */
    .stApp::after {{
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(9, 13, 22, 0.45);
        z-index: 0;
    }}
    
    .block-container {{
        position: relative;
        z-index: 1;
        padding-top: 3rem !important;
        padding-bottom: 1.5rem !important;
        max-width: 350px !important;
        margin: auto !important;
    }}
    
    #MainMenu, header, footer {{visibility: hidden;}}

    /* Form Container acting as Gorgeous Dark Glass Card */
    div[data-testid="stForm"] {{
        background: rgba(15, 23, 42, 0.88) !important;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 18px !important;
        padding: 20px 16px 16px 16px !important;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
    }}
    
    /* Hide Only Text Input Labels */
    div[data-testid="stTextInput"] label {{
        display: none !important;
    }}
    
    /* Inside Card Header Elements */
    .card-crest-box {{
        display: flex;
        justify-content: center;
        margin-bottom: 6px;
    }}
    
    .card-crest {{
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        width: 52px;
        height: 52px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 5px 14px rgba(0, 0, 0, 0.5), 0 0 0 3px rgba(255, 255, 255, 0.1);
        border: 2px solid rgba(255, 255, 255, 0.25);
        overflow: hidden;
    }}
    
    .card-crest img {{
        width: 100%;
        height: 100%;
        object-fit: cover;
    }}
    
    .card-title {{
        text-align: center;
        color: #FFFFFF !important;
        font-size: 1.15rem;
        font-weight: 800;
        letter-spacing: 0.5px;
        margin-bottom: 2px;
    }}
    
    .card-subtitle {{
        text-align: center;
        color: #94A3B8 !important;
        font-size: 0.6rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
        margin-bottom: 14px;
    }}
    
    /* Input Fields Design */
    .stTextInput>div>div>input {{
        background-color: rgba(30, 41, 59, 0.75) !important;
        color: #F8FAFC !important;
        font-weight: 500;
        border-radius: 8px;
        border: 1.5px solid rgba(255, 255, 255, 0.12);
        padding: 8px 12px;
        font-size: 0.82rem;
    }}
    
    .stTextInput>div>div>input::placeholder {{
        color: #94A3B8 !important;
    }}
    
    .stTextInput>div>div>input:focus {{
        background-color: rgba(30, 41, 59, 0.95) !important;
        border-color: #38BDF8 !important;
        box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.2);
    }}
    
    /* Checkbox & Links Fix */
    .stCheckbox {{
        min-height: unset !important;
    }}
    
    .stCheckbox label p {{
        color: #94A3B8 !important;
        font-weight: 500 !important;
        font-size: 0.72rem !important;
        white-space: nowrap !important;
    }}
    
    .forgot-pass {{
        color: #38BDF8;
        font-size: 0.72rem;
        font-weight: 500;
        text-decoration: none;
        white-space: nowrap !important;
        transition: color 0.2s;
    }}
    
    .forgot-pass:hover {{
        color: #60A5FA;
        text-decoration: underline;
    }}
    
    /* Submit Button */
    .stFormSubmitButton>button {{
        width: 100% !important;
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 0.85rem !important;
        letter-spacing: 1.2px;
        border: none !important;
        padding: 8px !important;
        border-radius: 8px !important;
        box-shadow: 0 5px 14px rgba(37, 99, 235, 0.4) !important;
        margin-top: 4px !important;
        transition: all 0.3s ease !important;
    }}
    
    .stFormSubmitButton>button:hover {{
        background: linear-gradient(135deg, #1D4ED8 100%, #1E40AF 100%) !important;
        transform: translateY(-1px);
        box-shadow: 0 7px 18px rgba(37, 99, 235, 0.6) !important;
    }}
    
    /* Footer */
    .portal-footer {{
        text-align: center;
        color: #CBD5E1;
        font-size: 10.5px;
        margin-top: 12px;
        font-weight: 600;
        letter-spacing: 0.5px;
        background: rgba(15, 23, 42, 0.75);
        padding: 5px 12px;
        border-radius: 7px;
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 5px 14px rgba(0, 0, 0, 0.4);
        width: fit-content;
        margin-left: auto;
        margin-right: auto;
    }}
    </style>
""", unsafe_allow_html=True)

# --- UI Render ---

if logo_image_data:
    logo_html = f"<div class='card-crest'><img src='{logo_image_data}' alt='IUBAT Logo'></div>"
else:
    logo_html = "<div class='card-crest'>🎓</div>"

with st.form("login_form"):
    st.markdown(f"""
        <div class='card-crest-box'>
            {logo_html}
        </div>
        <div class='card-title'>IUBAT Nexus</div>
        <div class='card-subtitle'>Smart Portal for Innovation & Academics</div>
    """, unsafe_allow_html=True)

    user_id = st.text_input("Your ID Number", placeholder="Your ID Number *")
    password = st.text_input("Password", type="password", placeholder="Password *")

    col1, col2 = st.columns([1.1, 1])
    with col1:
        remember_me = st.checkbox("Remember me")
    with col2:
        st.markdown("<div style='text-align: right; padding-top: 4px;'><a href='#' class='forgot-pass'>Forgot Password?</a></div>", unsafe_allow_html=True)

    submit_btn = st.form_submit_button("Login")
    if submit_btn:
        if user_id and password:
            st.success(f"Welcome back, {user_id}!")
        else:
            st.error("❌ Please enter both ID Number and Password.")

st.markdown("<div class='portal-footer'>Version: 1.0.0 Beta &nbsp;|&nbsp; © 2026 IUBAT Nexus</div>", unsafe_allow_html=True)
