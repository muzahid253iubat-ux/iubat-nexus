import streamlit as st
import os
import base64

# --- App Setup ---
st.set_page_config(
    page_title="IUBAT Nexus | Smart Portal",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Asset Readers ---
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
    return "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?auto=format&fit=crop&w=1950&q=80"

bg_image_data = get_fixed_background()
logo_image_data = get_asset_base64("logo.png")

# --- Custom Styling ---
st.markdown(f"""
    <style>
    .stApp {{
        background: #090D16;
    }}
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: url('{bg_image_data}') no-repeat center center fixed;
        background-size: cover;
        z-index: 0;
    }}
    .stApp::after {{
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(9, 13, 22, 0.55);
        z-index: 0;
    }}
    .block-container {{
        position: relative;
        z-index: 1;
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 420px !important;
        margin: auto !important;
    }}
    #MainMenu, header, footer {{visibility: hidden;}}

    /* Login Card */
    div[data-testid="stForm"] {{
        background: rgba(15, 23, 42, 0.90) !important;
        backdrop-filter: blur(14px);
        border-radius: 20px !important;
        padding: 24px 18px 18px 18px !important;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.7) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
    }}
    div[data-testid="stTextInput"] label {{
        display: none !important;
    }}
    .card-crest {{
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        width: 56px; height: 56px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        margin: 0 auto 8px auto;
        border: 2px solid rgba(255, 255, 255, 0.25);
        box-shadow: 0 5px 15px rgba(0,0,0,0.5);
        overflow: hidden;
    }}
    .card-crest img {{ width: 100%; height: 100%; object-fit: cover; }}
    .card-title {{ text-align: center; color: #FFFFFF !important; font-size: 1.25rem; font-weight: 800; margin-bottom: 2px; }}
    .card-subtitle {{ text-align: center; color: #94A3B8 !important; font-size: 0.65rem; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; margin-bottom: 16px; }}
    
    .stTextInput>div>div>input {{
        background-color: rgba(30, 41, 59, 0.8) !important;
        color: #F8FAFC !important; border-radius: 8px;
        border: 1.5px solid rgba(255, 255, 255, 0.12); padding: 9px 12px; font-size: 0.85rem;
    }}
    .stFormSubmitButton>button {{
        width: 100% !important;
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
        color: #FFFFFF !important; font-weight: 700; border-radius: 8px; border: none; padding: 9px;
    }}

    /* Dashboard Mobile UI Styles */
    .dashboard-header {{
        background: rgba(15, 23, 42, 0.85);
        backdrop-filter: blur(10px);
        padding: 12px 16px;
        border-radius: 14px;
        color: white;
        margin-bottom: 14px;
        border: 1px solid rgba(255,255,255,0.1);
    }}
    .sched-card {{
        background: rgba(15, 23, 42, 0.88);
        border-radius: 16px;
        padding: 16px;
        color: #F8FAFC;
        border: 1px solid rgba(255,255,255,0.12);
        box-shadow: 0 10px 25px rgba(0,0,0,0.4);
        margin-bottom: 14px;
    }}
    .badge-tag {{
        background: rgba(56, 189, 248, 0.15);
        color: #38BDF8;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.7rem;
        font-weight: 600;
    }}
    .route-stop {{
        padding: 6px 0;
        border-left: 2px solid #38BDF8;
        padding-left: 12px;
        margin-left: 6px;
        font-size: 0.8rem;
        color: #CBD5E1;
    }}
    </style>
""", unsafe_allow_html=True)

# --- Session Management ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_id" not in st.session_state:
    st.session_state.user_id = ""

# --- UI Views ---
logo_html = f"<div class='card-crest'><img src='{logo_image_data}' alt='Logo'></div>" if logo_image_data else "<div class='card-crest'>🎓</div>"

if not st.session_state.logged_in:
    with st.form("login_form"):
        st.markdown(f"{logo_html}<div class='card-title'>IUBAT Nexus</div><div class='card-subtitle'>Smart Portal for Innovation & Academics</div>", unsafe_allow_html=True)
        user_id = st.text_input("Your ID Number", placeholder="Your ID Number *")
        password = st.text_input("Password", type="password", placeholder="Password *")

        col1, col2 = st.columns([1.1, 1])
        with col1:
            st.checkbox("Remember me")
        with col2:
            st.markdown("<div style='text-align: right; padding-top: 4px;'><a href='#' style='color: #38BDF8; font-size: 0.72rem; text-decoration: none;'>Forgot Password?</a></div>", unsafe_allow_html=True)

        if st.form_submit_button("Login"):
            if user_id and password:
                st.session_state.logged_in = True
                st.session_state.user_id = user_id
                st.rerun()
            else:
                st.error("❌ Please enter both ID Number and Password.")
    st.markdown("<div style='text-align: center; color: #CBD5E1; font-size: 11px; margin-top: 15px;'>© 2026 IUBAT Nexus</div>", unsafe_allow_html=True)

else:
    # --- Authenticated Dashboard (App-like Transport View) ---
    st.markdown(f"""
        <div class='dashboard-header'>
            <div style='font-size: 0.75rem; color: #94A3B8;'>📍 Location</div>
            <div style='font-size: 0.95srem; font-weight: 700;'>Tongi Station Road / Uttara Campus</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🚌 Your Schedule")
    
    st.markdown("""
        <div class='sched-card'>
            <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;'>
                <span style='font-weight: 700; font-size: 0.95rem;'>Bus 02: Campus to Tongi & Gazipur</span>
                <span class='badge-tag'>Upcoming</span>
            </div>
            <div style='display: flex; justify-content: space-between; color: #94A3B8; font-size: 0.8rem; margin-bottom: 12px;'>
                <div>🕒 <b>05:30 PM</b><br>Departure</div>
                <div>➡️</div>
                <div>🕒 <b>07:30 PM</b><br>Arrival (ETA)</div>
            </div>
            <hr style='border-color: rgba(255,255,255,0.1); margin: 8px 0;'>
            <div style='font-size: 0.82rem; margin-top: 8px;'><b>Driver:</b> Sobuj Hossain (📞 01621796157)[cite: 16]</div>
            <div style='font-size: 0.82rem; margin-top: 4px;'><b>Helper:</b> Ripon (📞 01861455868)[cite: 16]</div>
        </div>
    """, unsafe_allow_html=True)

    with st.expander("🗺️ View Full Route Map Stoppages"):
        st.markdown("""
            <div class='route-stop'>📍 Campus (Uttara)</div>
            <div class='route-stop'>📍 Tongi Station Road[cite: 15]</div>
            <div class='route-stop'>📍 Amtoly Mor[cite: 15]</div>
            <div class='route-stop'>📍 T & T Bazar[cite: 15]</div>
            <div class='route-stop'>📍 Shilmoon[cite: 15]</div>
            <div class='route-stop'>📍 Nimtoly Bridge[cite: 15]</div>
            <div class='route-stop'>📍 Majukhan Bazar[cite: 15]</div>
            <div class='route-stop'>📍 Gazipur Chowrasta / Basugaon</div>
        """, unsafe_allow_html=True)

    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()
