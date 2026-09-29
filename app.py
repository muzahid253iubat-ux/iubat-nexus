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

# --- Custom CSS Matching UU App Layout Style ---
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
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        max-width: 420px !important;
    }}
    
    /* Phone Mockup Outer Frame */
    .phone-mockup {{
        background: #090D16;
        border-radius: 46px;
        padding: 14px;
        box-shadow: 0 30px 70px rgba(0, 0, 0, 0.9), 0 0 0 1px rgba(255, 255, 255, 0.1);
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
        padding: 2px 10px 10px 10px;
    }}
    
    /* Top Large Edge-to-Edge Banner like UU app */
    .phone-banner {{
        background: linear-gradient(rgba(15, 23, 42, 0.15), rgba(15, 23, 42, 0.55)), url('{bg_image_data}');
        background-size: cover;
        background-position: center;
        border-radius: 32px 32px 0 0;
        padding: 65px 16px 85px 16px;
        text-align: center;
        color: white;
        margin: -14px -14px 0 -14px;
        position: relative;
    }}
    
    .banner-top-title {{
        font-size: 1.05rem;
        font-weight: 700;
        color: #FFFFFF;
        letter-spacing: 0.5px;
        text-shadow: 0 2px 6px rgba(0,0,0,0.8);
    }}
    
    /* Overlapping Crest/Logo Box Style matching UU reference */
    .crest-container {{
        display: flex;
        justify-content: center;
        margin-top: -45px;
        position: relative;
        z-index: 10;
        margin-bottom: 8px;
    }}
    
    .crest-box {{
        background: #FFFFFF;
        width: 72px;
        height: 72px;
        border-radius: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
        border: 4px solid #FFFFFF;
        font-size: 36px;
    }}
    
    .university-heading {{
        text-align: center;
        color: #0F172A;
        font-size: 1.45rem;
        font-weight: 800;
        margin-top: 4px;
        letter-spacing: 0.3px;
    }}
    
    .university-subheading {{
        text-align: center;
        color: #64748B;
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 16px;
        font-weight: 600;
    }}
    
    /* Modern Solid White Form Card */
    div[data-testid="stForm"] {{
        background: #FFFFFF !important;
        padding: 8px 16px 20px 16px !important;
        border-radius: 0 0 32px 32px !important;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.25) !important;
        border: none !important;
    }}
    
    /* Label Styling */
    div[data-testid="stForm"] label p {{
        color: #0F172A !important;
        font-weight: 700 !important;
        font-size: 0.85rem !important;
    }}
    
    /* Input Fields Modern Look */
    .stTextInput>div>div>input {{
        background-color: #F8FAFC !important;
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
        margin-top: 8px !important;
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

# Top Large Picture Banner Section (Edge-to-Edge)
st.markdown("""
    <div class='phone-banner'>
        <div class='banner-top-title'>IUBAT Nexus</div>
    </div>
""", unsafe_allow_html=True)

# Overlapping Crest & University Info Box (UU Style)
st.markdown("""
    <div class='crest-container'>
        <div class='crest-box'>🎓</div>
    </div>
    <div class='university-heading'>IUBAT Nexus</div>
    <div class='university-subheading'>Excellence in Higher Education & Research</div>
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
