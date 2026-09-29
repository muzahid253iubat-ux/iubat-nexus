import streamlit as st
import os
import base64

# --- App Setup ---
st.set_page_config(
    page_title="IUBAT Nexus | Mobile Portal",
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

# --- Custom CSS for Mobile App Layout Simulation ---
st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(10, 15, 30, 0.5), rgba(10, 15, 30, 0.65)), 
                    url('{bg_image_data}');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-repeat: no-repeat;
    }}
    
    /* Mobile App Frame Container */
    .mobile-frame {{
        background: rgba(15, 23, 42, 0.85);
        padding: 30px 25px;
        border-radius: 35px;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.7);
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
        border: 2px solid rgba(255, 255, 255, 0.15);
        max-width: 410px;
        margin: 0 auto;
    }}
    
    /* Simulated Phone Status Bar */
    .status-bar {{
        display: flex;
        justify-content: space-between;
        color: #94A3B8;
        font-size: 13px;
        font-weight: 600;
        margin-bottom: 15px;
        padding: 0 5px;
    }}
    
    .app-logo-area {{
        text-align: center;
        margin-bottom: 10px;
    }}
    
    .app-logo-icon {{
        font-size: 40px;
        background: rgba(255, 255, 255, 0.1);
        display: inline-block;
        padding: 12px;
        border-radius: 20px;
        margin-bottom: 8px;
        border: 1px solid rgba(255, 255, 255, 0.15);
    }}
    
    .main-title {{
        font-size: 1.6rem;
        font-weight: 800;
        color: #FFFFFF;
        text-align: center;
        letter-spacing: 0.5px;
        margin-bottom: 2px;
    }}
    
    .sub-title {{
        color: #94A3B8 !important;
        text-align: center;
        font-size: 0.85rem;
        font-weight: 500;
        margin-bottom: 25px;
    }}
    
    label {{
        color: #E2E8F0 !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
    }}
    
    .stTextInput>div>div>input {{
        background-color: rgba(255, 255, 255, 0.95) !important;
        color: #0F172A !important;
        font-weight: 600;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        padding: 12px;
        font-size: 0.95rem;
    }}
    
    .stTextInput>div>div>input:focus {{
        border-color: #3B82F6;
        box-shadow: 0 0 10px rgba(59, 130, 246, 0.5);
    }}
    
    .stButton>button {{
        width: 100%;
        background: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%);
        color: white;
        font-weight: 700;
        font-size: 1rem;
        border: none;
        padding: 12px;
        border-radius: 12px;
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);
        transition: all 0.3s ease;
        margin-top: 5px;
    }}
    
    .stButton>button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.6);
        background: linear-gradient(135deg, #60A5FA 0%, #2563EB 100%);
    }}
    
    .app-footer {{
        text-align: center;
        color: rgba(255, 255, 255, 0.6);
        font-size: 11px;
        margin-top: 20px;
        letter-spacing: 0.3px;
    }}
    </style>
""", unsafe_allow_html=True)

# --- Main App Container (Mobile Frame Look) ---
with st.container():
    st.markdown("<div class='mobile-frame'>", unsafe_allow_html=True)
    
    # Fake mobile status bar
    st.markdown("<div class='status-bar'><span>6:44</span><span>📶 🔋 100%</span></div>", unsafe_allow_html=True)
    
    # App Logo and Title
    st.markdown("""
        <div class='app-logo-area'>
            <div class='app-logo-icon'>🎓</div>
            <div class='main-title'>IUBAT Nexus</div>
            <div class='sub-title'>Excellence in Higher Education & Research</div>
        </div>
    """, unsafe_allow_html=True)
    
    user_id = st.text_input("ID Number *", placeholder="e.g. 20103056")
    password = st.text_input("Password *", type="password", placeholder="••••••••")
    
    remember_me = st.checkbox("Remember me")
    
    st.write("")
    if st.button("Submit"):
        if user_id and password:
            st.success(f"Welcome back, {user_id}!")
        else:
            st.error("❌ Please enter both ID Number and Password.")
            
    st.markdown("<div class='app-footer'>Version : 1.0.0 Beta<br>© 2026 IUBAT Nexus</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
