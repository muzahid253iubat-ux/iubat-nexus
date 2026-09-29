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

# --- Custom CSS for Unique Modern Floating Card Design ---
st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.9), rgba(30, 41, 59, 0.95)), 
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
        max-width: 440px !important;
    }}
    
    /* Unique Master Container Card */
    .master-card {{
        background: #FFFFFF;
        border-radius: 28px;
        box-shadow: 0 30px 60px rgba(0, 0, 0, 0.5), 0 0 0 1px rgba(255, 255, 255, 0.15);
        overflow: hidden;
    }}
    
    /* Header Hero Section */
    .hero-banner {{
        background: linear-gradient(rgba(15, 23, 42, 0.3), rgba(15, 23, 42, 0.75)), url('{bg_image_data}');
        background-size: cover;
        background-position: center;
        padding: 50px 20px 40px 20px;
        text-align: center;
        color: white;
    }}
    
    .hero-title {{
        font-size: 1.4rem;
        font-weight: 800;
        letter-spacing: 0.5px;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.8);
    }}
    
    .hero-subtitle {{
        font-size: 0.75rem;
        color: #CBD5E1;
        margin-top: 4px;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
        text-shadow: 0 1px 4px rgba(0, 0, 0, 0.8);
    }}
    
    /* Floating Icon Badge */
    .badge-wrapper {{
        display: flex;
        justify-content: center;
        margin-top: -30px;
        position: relative;
        z-index: 5;
        margin-bottom: 10px;
    }}
    
    .badge-icon {{
        background: #0F172A;
        color: #FFFFFF;
        width: 60px;
        height: 60px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 10px 20px rgba(15, 23, 42, 0.3);
        border: 4px solid #FFFFFF;
        font-size: 26px;
    }}
    
    /* Form Padding inside Master Card */
    div[data-testid="stForm"] {{
        background: #FFFFFF !important;
        padding: 0px 28px 24px 28px !important;
        border: none !important;
        box-shadow: none !important;
    }}
    
    /* Label Styling */
    div[data-testid="stForm"] label p {{
        color: #0F172A !important;
        font-weight: 700 !important;
        font-size: 0.85rem !important;
    }}
    
    /* Input Fields */
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
    
    /* Checkbox */
    .stCheckbox label p {{
        color: #334155 !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
    }}
    
    /* Submit Button */
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
    
    /* Seamless Footer inside Master Card */
    .card-footer {{
        text-align: center;
        color: #64748B;
        font-size: 11px;
        padding: 0px 0px 24px 0px;
        font-weight: 500;
        background: #FFFFFF;
        letter-spacing: 0.3px;
    }}
    </style>
""", unsafe_allow_html=True)

# --- UI Render ---
st.markdown("<div class='master-card'>", unsafe_allow_html=True)

# Hero Header with Banner Background
st.markdown("""
    <div class='hero-banner'>
        <div class='hero-title'>IUBAT Nexus</div>
        <div class='hero-subtitle'>Excellence in Higher Education & Research</div>
    </div>
""", unsafe_allow_html=True)

# Floating Badge Icon
st.markdown("""
    <div class='badge-wrapper'>
        <div class='badge-icon'>🎓</div>
    </div>
""", unsafe_allow_html=True)

# Form
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

# Seamless Footer inside the same card
st.markdown("<div class='card-footer'>Version : 1.0.0 Beta<br>© 2026 IUBAT Nexus</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
