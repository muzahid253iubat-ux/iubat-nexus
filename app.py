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

# --- Custom CSS Matching Reference Floating Minimal Card Style ---
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
        padding-top: 4rem !important;
        padding-bottom: 2rem !important;
        max-width: 440px !important;
    }}
    
    /* Floating Avatar Circle centered on top of card */
    .avatar-container {{
        display: flex;
        justify-content: center;
        margin-bottom: -40px;
        position: relative;
        z-index: 10;
    }}
    
    .avatar-circle {{
        background: #0F172A;
        width: 80px;
        height: 80px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.35), 0 0 0 6px rgba(255, 255, 255, 0.2);
        border: 4px solid #FFFFFF;
        font-size: 36px;
    }}
    
    /* Main Floating Card */
    .floating-card {{
        background: #FFFFFF;
        border-radius: 24px;
        padding: 50px 30px 30px 30px;
        box-shadow: 0 25px 60px rgba(0, 0, 0, 0.45);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }}
    
    .card-heading {{
        text-align: center;
        color: #0F172A;
        font-size: 1.25rem;
        font-weight: 800;
        margin-bottom: 4px;
    }}
    
    .card-subheading {{
        text-align: center;
        color: #64748B;
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 24px;
        font-weight: 600;
    }}
    
    /* Form Styling */
    div[data-testid="stForm"] {{
        background: transparent !important;
        padding: 0px !important;
        border: none !important;
        box-shadow: none !important;
    }}
    
    /* Label hiding for clean minimal look */
    div[data-testid="stForm"] label p {{
        display: none !important;
    }}
    
    /* Input Fields Styling */
    .stTextInput>div>div>input {{
        background-color: #F1F5F9 !important;
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
    
    /* Checkbox Styling */
    .stCheckbox label p {{
        display: block !important;
        color: #475569 !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
    }}
    
    /* Login Submit Button Matching Reference Style */
    .stFormSubmitButton>button {{
        width: 100% !important;
        background: #0F172A !important;
        color: white !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        letter-spacing: 1px;
        border: none !important;
        padding: 13px !important;
        border-radius: 10px !important;
        box-shadow: 0 6px 18px rgba(15, 23, 42, 0.3) !important;
        margin-top: 12px !important;
        transition: all 0.3s ease !important;
    }}
    
    .stFormSubmitButton>button:hover {{
        background: #1E293B !important;
        box-shadow: 0 8px 22px rgba(15, 23, 42, 0.4) !important;
        transform: translateY(-1px);
    }}
    
    .portal-footer {{
        text-align: center;
        color: #64748B;
        font-size: 11px;
        margin-top: 24px;
        font-weight: 500;
        letter-spacing: 0.3px;
    }}
    </style>
""", unsafe_allow_html=True)

# --- UI Render ---
# Floating Avatar Circle
st.markdown("""
    <div class='avatar-container'>
        <div class='avatar-circle'>👤</div>
    </div>
""", unsafe_allow_html=True)

# Floating Card Container
st.markdown("<div class='floating-card'>", unsafe_allow_html=True)

st.markdown("""
    <div class='card-heading'>IUBAT Nexus</div>
    <div class='card-subheading'>Portal Login</div>
""", unsafe_allow_html=True)

# Form
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
