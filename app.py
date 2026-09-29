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

# --- Custom CSS for Top Banner + Bottom Clean Card Layout ---
st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(10, 15, 30, 0.7), rgba(10, 15, 30, 0.85)), 
                    url('{bg_image_data}');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-repeat: no-repeat;
    }}
    
    #MainMenu, header, footer {{visibility: hidden;}}
    
    .block-container {{
        padding-top: 1.5rem !important;
        padding-bottom: 1.5rem !important;
        max-width: 420px !important;
    }}
    
    /* Phone Mockup Outer Frame */
    .phone-mockup {{
        background: #0F172A;
        border-radius: 40px;
        padding: 12px 12px 20px 12px;
        box-shadow: 0 30px 70px rgba(0, 0, 0, 0.85);
        border: 4px solid #334155;
        overflow: hidden;
    }}
    
    /* Phone Status Bar */
    .status-bar {{
        display: flex;
        justify-content: space-between;
        color: #FFFFFF;
        font-size: 13px;
        font-weight: 600;
        padding: 5px 15px 12px 15px;
    }}
    
    /* Top Picture Banner inside phone */
    .phone-banner {{
        background: linear-gradient(rgba(0, 0, 0, 0.35), rgba(0, 0, 0, 0.55)), url('{bg_image_data}');
        background-size: cover;
        background-position: center;
        border-radius: 20px;
        padding: 30px 15px;
        text-align: center;
        color: white;
        margin-bottom: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }}
    
    .banner-title {{
        font-size: 1.4rem;
        font-weight: 800;
        margin-top: 8px;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.8);
    }}
    
    .banner-sub {{
        font-size: 0.75rem;
        color: #E2E8F0;
        margin-top: 4px;
        text-shadow: 0 1px 5px rgba(0, 0, 0, 0.8);
    }}
    
    /* White Card for Form Inputs Below */
    .login-card {{
        background: #FFFFFF;
        padding: 22px 18px;
        border-radius: 24px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
        color: #0F172A;
    }}
    
    label {{
        color: #334155 !important;
        font-weight: 700 !important;
        font-size: 0.85rem !important;
    }}
    
    .stTextInput>div>div>input {{
        background-color: #F8FAFC !important;
        color: #0F172A !important;
        font-weight: 600;
        border-radius: 10px;
        border: 1px solid #CBD5E1;
        padding: 10px;
        font-size: 0.9rem;
    }}
    
    .stTextInput>div>div>input:focus {{
        border-color: #1E293B;
        box-shadow: 0 0 0 2px rgba(30, 41, 59, 0.15);
    }}
    
    .stButton>button {{
        width: 100%;
        background: #1E293B;
        color: white;
        font-weight: 700;
        font-size: 0.95rem;
        border: none;
        padding: 11px;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(30, 41, 59, 0.3);
        margin-top: 5px;
        transition: all 0.2s ease;
    }}
    
    .stButton>button:hover {{
        background: #0F172A;
    }}
    
    .phone-footer {{
        text-align: center;
        color: #94A3B8;
        font-size: 11px;
        margin-top: 15px;
        font-weight: 500;
    }}
    </style>
""", unsafe_allow_html=True)

# --- UI Render ---
st.markdown("<div class='phone-mockup'>", unsafe_allow_html=True)

# Status bar
st.markdown("<div class='status-bar'><span>4:51</span><span>📶 🔋 100%</span></div>", unsafe_allow_html=True)

# Top Picture Banner Section
st.markdown("""
    <div class='phone-banner'>
        <div style='font-size: 32px;'>🎓</div>
        <div class='banner-title'>IUBAT Nexus</div>
        <div class='banner-sub'>Excellence in Higher Education & Research</div>
    </div>
""", unsafe_allow_html=True)

# Bottom Login Card Section
st.markdown("<div class='login-card'>", unsafe_allow_html=True)

user_id = st.text_input("ID Number *", placeholder="e.g. 20103056")
password = st.text_input("Password *", type="password", placeholder="••••••••")

remember_me = st.checkbox("Remember me")

st.write("")
if st.button("Submit"):
    if user_id and password:
        st.success(f"Welcome back, {user_id}!")
    else:
        st.error("❌ Please enter both ID Number and Password.")

st.markdown("</div>", unsafe_allow_html=True)

# Footer inside phone mockup
st.markdown("<div class='phone-footer'>Version : 1.0.0 Beta<br>© 2026 IUBAT Nexus</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
