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

# --- Custom CSS for Clean Professional Card Layout ---
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
    
    /* Main Portal Card Container */
    .portal-card {{
        background: #FFFFFF;
        border-radius: 24px;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.4);
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }}
    
    /* Banner Header */
    .portal-banner {{
        background: linear-gradient(rgba(15, 23, 42, 0.2), rgba(15, 23, 42, 0.6)), url('{bg_image_data}');
        background-size: cover;
        background-position: center;
        padding: 45px 20px 55px 20px;
        text-align: center;
        color: white;
        position: relative;
    }}
    
    .banner-title {{
        font-size: 1.2rem;
        font-weight: 700;
        color: #FFFFFF;
        letter-spacing: 0.5px;
        text-shadow: 0 2px 4px rgba(0,0,0,0.6);
    }}
    
    /* Overlapping Crest/Logo Box */
    .crest-container {{
        display: flex;
        justify-content: center;
        margin-top: -38px;
        position: relative;
        z-index: 10;
        margin-bottom: 8px;
    }}
    
    .crest-box {{
        background: #FFFFFF;
        width: 68px;
        height: 68px;
        border-radius: 18px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
        border: 3px solid #FFFFFF;
        font-size: 32px;
    }}
    
    .university-heading {{
        text-align: center;
        color: #0F172A;
        font-size: 1.35rem;
        font-weight: 800;
        margin-top: 4px;
        letter-spacing: 0.3px;
    }}
    
    .university-subheading {{
        text-align: center;
        color: #64748B;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 20px;
        font-weight: 600;
    }}
    
    /* Form Padding inside Card */
    div[data-testid="stForm"] {{
        background: #FFFFFF !important;
        padding: 0px 24px 24px 24px !important;
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
    
    .portal-footer {{
        text-align: center;
        color: #64748B;
        font-size: 11px;
        padding-bottom: 20px;
        font-weight: 500;
        background: #FFFFFF;
    }}
    </style>
""", unsafe_allow_html=True)

# --- UI Render ---
st.markdown("<div class='portal-card'>", unsafe_allow_html=True)

# Top Banner
st.markdown("""
    <div class='portal-banner'>
        <div class='banner-title'>IUBAT Nexus</div>
    </div>
""", unsafe_allow_html=True)

# Crest & Headings
st.markdown("""
    <div class='crest-container'>
        <div class='crest-box'>🎓</div>
    </div>
    <div class='university-heading'>IUBAT Nexus</div>
    <div class='university-subheading'>Excellence in Higher Education & Research</div>
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

# Footer
st.markdown("<div class='portal-footer'>Version : 1.0.0 Beta<br>© 2026 IUBAT Nexus</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
