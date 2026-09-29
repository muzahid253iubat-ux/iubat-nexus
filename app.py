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

# --- Custom CSS for Exact Smartphone Mockup & UI Styling ---
st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(10, 15, 30, 0.4), rgba(10, 15, 30, 0.6)), 
                    url('{bg_image_data}');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-repeat: no-repeat;
    }}
    
    #MainMenu, header, footer {{visibility: hidden;}}
    
    .block-container {{
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 420px !important;
    }}
    
    /* Phone Mockup Outer Frame */
    .phone-mockup {{
        background: #0F172A;
        border-radius: 45px;
        padding: 15px 15px 25px 15px;
        box-shadow: 0 30px 70px rgba(0, 0, 0, 0.85);
        border: 4px solid #334155;
    }}
    
    /* Phone Status Bar */
    .status-bar {{
        display: flex;
        justify-content: space-between;
        color: #FFFFFF;
        font-size: 13px;
        font-weight: 600;
        padding: 5px 15px 10px 15px;
    }}
    
    /* Inner Card matching reference style */
    .login-card {{
        background: #FFFFFF;
        padding: 28px 22px;
        border-radius: 30px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        color: #0F172A;
    }}
    
    .crest-box {{
        text-align: center;
        margin-bottom: 12px;
    }}
    
    .crest-icon {{
        font-size: 36px;
        background: #F1F5F9;
        display: inline-block;
        padding: 10px 14px;
        border-radius: 16px;
        border: 1px solid #E2E8F0;
    }}
    
    .portal-title {{
        font-size: 1.45rem;
        font-weight: 800;
        color: #0F172A;
        text-align: center;
        margin-bottom: 2px;
        letter-spacing: 0.3px;
    }}
    
    .portal-subtitle {{
        color: #64748B;
        text-align: center;
        font-size: 0.75rem;
        font-weight: 600;
        margin-bottom: 22px;
    }}
    
    label {{
        color: #334155 !important;
        font-weight: 700 !important;
        font-size: 0.88rem !important;
    }}
    
    .stTextInput>div>div>input {{
        background-color: #F8FAFC !important;
        color: #0F172A !important;
        font-weight: 600;
        border-radius: 12px;
        border: 1px solid #CBD5E1;
        padding: 11px;
        font-size: 0.92rem;
    }}
    
    .stTextInput>div>div>input:focus {{
        border-color: #1E293B;
        box-shadow: 0 0 0 2px rgba(30, 41, 59, 0.15);
    }}
    
    .stCheckbox {{
        margin-top: -5px;
        margin-bottom: 5px;
    }}
    
    .stButton>button {{
        width: 100%;
        background: #1E293B;
        color: white;
        font-weight: 700;
        font-size: 0.98rem;
        border: none;
        padding: 12px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(30, 41, 59, 0.3);
        transition: all 0.2s ease;
        margin-top: 5px;
    }}
    
    .stButton>button:hover {{
        background: #0F172A;
        box-shadow: 0 6px 18px rgba(15, 23, 42, 0.4);
    }}
    
    .phone-footer {{
        text-align: center;
        color: #64748B;
        font-size: 11px;
        margin-top: 20px;
        font-weight: 500;
        line-height: 1.4;
    }}
    </style>
""", unsafe_allow_html=True)

# --- UI Render ---
st.markdown("<div class='phone-mockup'>", unsafe_allow_html=True)

# Status bar
st.markdown("<div class='status-bar'><span>4:51</span><span>📶 🔋 100%</span></div>", unsafe_allow_html=True)

# White inner card container
st.markdown("<div class='login-card'>", unsafe_allow_html=True)

st.markdown("""
    <div class='crest-box'>
        <div class='crest-icon'>🛡️</div>
        <div class='portal-title'>IUBAT Nexus</div>
        <div class='portal-subtitle'>Excellence in Higher Education & Research</div>
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

st.markdown("</div>", unsafe_allow_html=True) # End login-card

# Footer inside phone mockup
st.markdown("<div class='phone-footer'>Version : 1.0.0 Beta<br>© 2026 IUBAT Nexus</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True) # End phone-mockup
