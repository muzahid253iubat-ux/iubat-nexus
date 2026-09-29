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

# --- Custom CSS for Unique & Modern UI ---
st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.85), rgba(30, 41, 59, 0.95)), 
                    url('{bg_image_data}');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-repeat: no-repeat;
    }}
    
    #MainMenu, header, footer {{visibility: hidden;}}
    
    .block-container {{
        padding-top: 1.2rem !important;
        padding-bottom: 1.2rem !important;
        max-width: 420px !important;
    }}
    
    /* Phone Mockup Outer Frame */
    .phone-mockup {{
        background: #090D16;
        border-radius: 44px;
        padding: 14px 14px 22px 14px;
        box-shadow: 0 25px 60px rgba(0, 0, 0, 0.9), 0 0 0 1px rgba(255, 255, 255, 0.1);
        border: 4px solid #1E293B;
        overflow: hidden;
    }}
    
    /* Phone Status Bar */
    .status-bar {{
        display: flex;
        justify-content: space-between;
        color: #F8FAFC;
        font-size: 13px;
        font-weight: 600;
        padding: 4px 16px 14px 16px;
    }}
    
    /* Top Picture Banner with Luxury Overlay */
    .phone-banner {{
        background: linear-gradient(rgba(15, 23, 42, 0.5), rgba(15, 23, 42, 0.75)), url('{bg_image_data}');
        background-size: cover;
        background-position: center;
        border-radius: 22px;
        padding: 24px 16px;
        text-align: center;
        color: white;
        margin-bottom: 14px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        box-shadow: 0 8px 20px rgba(0,0,0,0.3);
    }}
    
    .banner-icon {{
        font-size: 28px;
        background: rgba(255, 255, 255, 0.15);
        width: 50px;
        height: 50px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        margin-bottom: 6px;
        backdrop-filter: blur(4px);
    }}
    
    .banner-title {{
        font-size: 1.35rem;
        font-weight: 800;
        letter-spacing: 0.5px;
        margin-top: 2px;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.8);
    }}
    
    .banner-sub {{
        font-size: 0.72rem;
        color: #CBD5E1;
        margin-top: 3px;
        text-shadow: 0 1px 4px rgba(0, 0, 0, 0.8);
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    
    /* Modern Solid White Form Card */
    div[data-testid="stForm"] {{
        background: #FFFFFF !important;
        padding: 24px 20px !important;
        border-radius: 26px !important;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.25) !important;
        border: none !important;
    }}
    
    /* Label Styling */
    div[data-testid="stForm"] label p {{
        color: #0F172A !important;
        font-weight: 700 !important;
        font-size: 0.85rem !important;
        letter-spacing: 0.2px;
    }}
    
    /* Input Fields Modern Look */
    .stTextInput>div>div>input {{
        background-color: #F1F5F9 !important;
        color: #0F172A !important;
        font-weight: 600;
        border-radius: 12px;
        border: 1.5px solid #E2E8F0;
        padding: 11px 14px;
        font-size: 0.9rem;
        transition: all 0.3s ease;
    }}
    
    .stTextInput>div>div>input:focus {{
        background-color: #FFFFFF !important;
        border-color: #0284C7;
        box-shadow: 0 0 0 3px rgba(2, 132, 199, 0.15);
    }}
    
    /* Checkbox Styling */
    .stCheckbox label p {{
        color: #334155 !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
    }}
    
    /* Unique Gradient Submit Button */
    .stFormSubmitButton>button {{
        width: 100% !important;
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.5px;
        border: none !important;
        padding: 12px !important;
        border-radius: 12px !important;
        box-shadow: 0 6px 18px rgba(15, 23, 42, 0.35) !important;
        margin-top: 10px !important;
        transition: all 0.3s ease !important;
    }}
    
    .stFormSubmitButton>button:hover {{
        background: linear-gradient(135deg, #1E293B 0%, #0284C7 100%) !important;
        box-shadow: 0 8px 22px rgba(2, 132, 199, 0.4) !important;
        transform: translateY(-1px);
    }}
    
    .phone-footer {{
        text-align: center;
        color: #64748B;
        font-size: 11px;
        margin-top: 16px;
        font-weight: 500;
        letter-spacing: 0.3px;
    }}
    </style>
""", unsafe_allow_html=True)

# --- UI Render ---
st.markdown("<div class='phone-mockup'>", unsafe_allow_html=True)

# Status bar
st.markdown("<div class='status-bar'><span>4:51</span><span>📶 🔋 100%</span></div>", unsafe_allow_html=True)

# Top Picture Banner Section with Icon
st.markdown("""
    <div class='phone-banner'>
        <div class='banner-icon'>🎓</div>
        <div class='banner-title'>IUBAT Nexus</div>
        <div class='banner-sub'>Excellence in Higher Education & Research</div>
    </div>
""", unsafe_allow_html=True)

# Form Container acting as a clean solid white card
with st.form("login_form"):
    user_id = st.text_input("ID Number *", placeholder="e.g. 20103056")
    password = st.text_input("Password *", type="password", placeholder="••••••••")

    remember_me = st.checkbox("Remember me")

    submit_btn = st.form_submit_button("Sign In")
    if submit_btn:
        if user_id and password:
            st.success(f"Welcome back, {user_id}!")
        else:
            st.error("❌ Please enter both ID Number and Password.")

# Footer inside phone mockup
st.markdown("<div class='phone-footer'>Version : 1.0.0 Beta<br>© 2026 IUBAT Nexus</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
