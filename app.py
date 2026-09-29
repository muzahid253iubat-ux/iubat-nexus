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

# --- Custom CSS for Balanced Blur & Dark Glass Theme ---
st.markdown(f"""
    <style>
    .stApp {{
        background: #090D16;
    }}
    
    /* Background Image with Balanced Subtle Blur */
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: url('{bg_image_data}') no-repeat center center fixed;
        background-size: cover;
        filter: blur(1.0px);
        -webkit-filter: blur(1.0px);
        transform: scale(1.05);
        z-index: 0;
    }}
    
    /* Balanced Dark Overlay for Crystal Clear Visibility */
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
        padding-top: 4.5rem !important;
        padding-bottom: 3rem !important;
        max-width: 440px !important;
    }}
    
    #MainMenu, header, footer {{visibility: hidden;}}

    /* Form Container acting as Gorgeous Dark Glass Card */
    div[data-testid="stForm"] {{
        background: rgba(15, 23, 42, 0.88) !important;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 24px !important;
        padding: 35px 32px 32px 32px !important;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
    }}
    
    div[data-testid="stForm"] label p {{
        display: none !important;
    }}
    
    /* Inside Card Header Elements */
    .card-crest-box {{
        display: flex;
        justify-content: center;
        margin-bottom: 12px;
    }}
    
    .card-crest {{
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        width: 72px;
        height: 72px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.5), 0 0 0 4px rgba(255, 255, 255, 0.1);
        border: 2px solid rgba(255, 255, 255, 0.25);
        color: #FFFFFF;
        font-size: 32px;
    }}
    
    .card-title {{
        text-align: center;
        color: #FFFFFF !important;
        font-size: 1.5rem;
        font-weight: 800;
        letter-spacing: 0.5px;
        margin-bottom: 2px;
    }}
    
    .card-subtitle {{
        text-align: center;
        color: #94A3B8 !important;
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        font-weight: 600;
        margin-bottom: 28px;
    }}
    
    /* Input Fields Design */
    .stTextInput>div>div>input {{
        background-color: rgba(30, 41, 59, 0.75) !important;
        color: #F8FAFC !important;
        font-weight: 500;
        border-radius: 10px;
        border: 1.5px solid rgba(255, 255, 255, 0.12);
        padding: 12px 16px;
        font-size: 0.95rem;
    }}
    
    .stTextInput>div>div>input::placeholder {{
        color: #94A3B8 !important;
    }}
    
    .stTextInput>div>div>input:focus {{
        background-color: rgba(30, 41, 59, 0.95) !important;
        border-color: #38BDF8 !important;
        box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.2);
    }}
    
    /* Checkbox & Links */
    .stCheckbox label p {{
        display: block !important;
        color: #94A3B8 !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
    }}
    
    .forgot-pass {{
        color: #38BDF8;
        font-size: 0.85rem;
        font-weight: 500;
        text-decoration: none;
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
        font-size: 1rem !important;
        letter-spacing: 1.5px;
        border: none !important;
        padding: 13px !important;
        border-radius: 10px !important;
        box-shadow: 0 8px 20px rgba(37, 99, 235, 0.4) !important;
        margin-top: 10px !important;
        transition: all 0.3s ease !important;
    }}
    
    .stFormSubmitButton>button:hover {{
        background: linear-gradient(135deg, #1D4ED8 0%, #1E40AF 100%) !important;
        transform: translateY(-1px);
        box-shadow: 0 10px 25px rgba(37, 99, 235, 0.6) !important;
    }}
    
    .portal-footer {{
        text-align: center;
        color: #94A3B8;
        font-size: 11px;
        margin-top: 25px;
        font-weight: 500;
        letter-spacing: 0.3px;
        text-shadow: 0 1px 3px rgba(0, 0, 0, 0.8);
    }}
    </style>
""", unsafe_allow_html=True)

# --- UI Render ---

# Login Form
with st.form("login_form"):
    st.markdown("""
        <div class='card-crest-box'>
            <div class='card-crest'>🎓</div>
        </div>
        <div class='card-title'>IUBAT Nexus</div>
        <div class='card-subtitle'>SMART PORTAL FOR INNOVATION & ACADEMICS</div>
    """, unsafe_allow_html=True)

    user_id = st.text_input("Your ID Number", placeholder="Your ID Number *")
    password = st.text_input("Password", type="password", placeholder="🔒 Password *")

    col1, col2 = st.columns([1.2, 1])
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

# Footer
st.markdown("<div class='portal-footer'>Version: 1.0.0 Beta<br>© 2026 IUBAT Nexus</div>", unsafe_allow_html=True)
