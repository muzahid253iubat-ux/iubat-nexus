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

# --- Ultra-Fast Cached Asset Reader ---
@st.cache_data(show_spinner=False)
def get_asset_base64_cached(filename):
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

@st.cache_data(show_spinner=False)
def get_fixed_background_cached():
    bg_data = get_asset_base64_cached("bp.jpg")
    if bg_data:
        return bg_data
    return "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?auto=format&fit=crop&w=1950&q=80"

bg_image_data = get_fixed_background_cached()
logo_image_data = get_asset_base64_cached("logo.png")

# --- Persistent Session & Remember Me Check ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_id" not in st.session_state:
    st.session_state.user_id = ""
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Home"

query_params = st.query_params
if not st.session_state.logged_in and "session_user" in query_params:
    st.session_state.logged_in = True
    st.session_state.user_id = query_params["session_user"]

# --- Google-Inspired Dynamic Styling ---
if not st.session_state.logged_in:
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
            background: rgba(9, 13, 22, 0.75);
            z-index: 0;
        }}
        .block-container {{
            position: relative;
            z-index: 1;
            padding-top: 2rem !important;
            max-width: 440px !important;
            margin: auto !important;
        }}
        #MainMenu, header, footer {{visibility: hidden;}}

        /* Google Style Floating Icons Showcase Header */
        .hero-showcase {{
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 16px;
            margin-bottom: 20px;
        }}
        .floating-badge {{
            width: 42px; height: 42px;
            background: rgba(30, 41, 59, 0.85);
            border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            box-shadow: 0 8px 20px rgba(0,0,0,0.4);
            border: 1px solid rgba(255,255,255,0.15);
            font-size: 1.1rem;
            animation: float 3s ease-in-out infinite;
        }}
        .floating-badge:nth-child(even) {{
            animation-delay: 1.5s;
        }}
        @keyframes float {{
            0%, 100% {{ transform: translateY(0); }}
            50% {{ transform: translateY(-6px); }}
        }}

        .central-avatar {{
            width: 80px; height: 80px;
            background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
            border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            box-shadow: 0 10px 30px rgba(37, 99, 235, 0.4);
            border: 2.5px solid rgba(56, 189, 248, 0.6);
            overflow: hidden;
        }}
        .central-avatar img {{ width: 100%; height: 100%; object-fit: cover; }}

        .hero-title {{
            text-align: center;
            color: #F8FAFC !important;
            font-size: 1.8rem;
            font-weight: 800;
            line-height: 1.2;
            margin-bottom: 8px;
            letter-spacing: -0.5px;
        }}
        .hero-subtitle {{
            text-align: center;
            color: #94A3B8 !important;
            font-size: 0.82rem;
            line-height: 1.4;
            margin-bottom: 24px;
            padding: 0 10px;
        }}

        div[data-testid="stForm"] {{
            background: rgba(15, 23, 42, 0.88) !important;
            backdrop-filter: blur(16px);
            border-radius: 20px !important;
            padding: 20px 20px 16px 20px !important;
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.7) !important;
            border: 1px solid rgba(255, 255, 255, 0.12) !important;
        }}
        div[data-testid="stTextInput"] label {{
            display: none !important;
        }}
        .stTextInput>div>div>input {{
            background-color: rgba(30, 41, 59, 0.8) !important;
            color: #F8FAFC !important; border-radius: 8px;
            border: 1.5px solid rgba(255, 255, 255, 0.12); padding: 9px 12px; font-size: 0.85rem;
        }}
        .stFormSubmitButton>button {{
            width: 100% !important;
            background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
            color: #FFFFFF !important; font-weight: 700; border-radius: 8px; border: none; padding: 10px;
        }}
        </style>
    """, unsafe_allow_html=True)

else:
    st.markdown("""
        <style>
        .stApp {
            background: #0F172A !important;
        }
        .block-container {
            position: relative;
            z-index: 1;
            padding-top: 1.5rem !important;
            padding-bottom: 2rem !important;
            max-width: 420px !important;
            margin: auto !important;
        }
        #MainMenu, header, footer {visibility: hidden;}

        .app-header {
            background: rgba(30, 41, 59, 0.7);
            backdrop-filter: blur(10px);
            padding: 14px 18px;
            border-radius: 16px;
            color: white;
            margin-bottom: 16px;
            border: 1px solid rgba(255,255,255,0.08);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .sched-card {
            background: rgba(30, 41, 59, 0.75);
            border-radius: 14px;
            padding: 14px;
            color: #F8FAFC;
            border: 1px solid rgba(255,255,255,0.1);
            margin-bottom: 10px;
        }
        .badge-tag {
            background: rgba(56, 189, 248, 0.15);
            color: #38BDF8;
            padding: 3px 8px;
            border-radius: 6px;
            font-size: 0.7rem;
            font-weight: 600;
        }
        .route-stop {
            padding: 6px 0;
            border-left: 2px solid #38BDF8;
            padding-left: 12px;
            margin-left: 6px;
            font-size: 0.8rem;
            color: #CBD5E1;
        }
        </style>
    """, unsafe_allow_html=True)


# --- UI Render ---
avatar_html = f"<div class='central-avatar'><img src='{logo_image_data}' alt='Logo'></div>" if logo_image_data else "<div class='central-avatar'>🎓</div>"

if not st.session_state.logged_in:
    # Google-inspired floating banner & header
    st.markdown(f"""
        <div class="hero-showcase">
            <div class="floating-badge" title="Emergency SOS">🚨</div>
            <div class="floating-badge" title="Faculty Directory">👨‍🏫</div>
            {avatar_html}
            <div class="floating-badge" title="Bus Tracking">🚌</div>
            <div class="floating-badge" title="Alumni Network">🎓</div>
        </div>
        <div class="hero-title">All of IUBAT,<br>working for you</div>
        <div class="hero-subtitle">Sign in to your Student Portal for seamless access to campus services, schedules, and academic tools from anywhere.</div>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        user_id = st.text_input("Your ID Number", placeholder="Your ID Number *")
        password = st.text_input("Password", type="password", placeholder="Password *")

        col1, col2 = st.columns([1.1, 1])
        with col1:
            remember_me = st.checkbox("Remember me")
        with col2:
            st.markdown("<div style='text-align: right; padding-top: 4px;'><a href='#' style='color: #38BDF8; font-size: 0.72rem; text-decoration: none;'>Forgot Password?</a></div>", unsafe_allow_html=True)

        if st.form_submit_button("Sign In"):
            if user_id and password:
                st.session_state.logged_in = True
                st.session_state.user_id = user_id
                st.session_state.active_tab = "Home"
                if remember_me:
                    st.query_params["session_user"] = user_id
                st.rerun()
            else:
                st.error("❌ Please enter both ID Number and Password.")
                
    st.markdown("<div style='text-align: center; color: #94A3B8; font-size: 11px; margin-top: 20px;'>© 2026 IUBAT Nexus • Secure Portal</div>", unsafe_allow_html=True)

else:
    st.markdown(f"""
        <div class='app-header'>
            <div>
                <div style='font-size: 0.7rem; color: #94A3B8;'>Welcome back,</div>
                <div style='font-size: 1.05rem; font-weight: 800; color: #F8FAFC;'>ID: {st.session_state.user_id}</div>
            </div>
            <div>
                <span class='badge-tag'>🟢 Online</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if st.session_state.active_tab != "Home":
        if st.button("⬅️ Back to Dashboard"):
            st.session_state.active_tab = "Home"
            st.rerun()

    if st.session_state.active_tab == "Home":
        st.markdown("<div style='font-size: 0.9rem; font-weight: 700; color: #94A3B8; margin-bottom: 10px;'>QUICK SERVICES</div>", unsafe_allow_html=True)

        if st.button("🚨  Emergency SOS & Security Hotline", use_container_width=True):
            st.session_state.active_tab = "SOS"
            st.rerun()

        if st.button("👨‍🏫  Faculty Directory & Consultations", use_container_width=True):
            st.session_state.active_tab = "Faculty"
            st.rerun()

        if st.button("🚌  Bus Schedule & Live Tracking", use_container_width=True):
            st.session_state.active_tab = "Bus"
            st.rerun()

        if st.button("🎓  Alumni Network & Mentorship", use_container_width=True):
            st.session_state.active_tab = "Alumni"
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚪 Logout from Portal", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.active_tab = "Home"
            if "session_user" in st.query_params:
                del st.query_params["session_user"]
            st.rerun()

    elif st.session_state.active_tab == "SOS":
        st.markdown("### 🚨 Emergency SOS & Hotline")
        st.markdown("If you are facing an emergency on campus or around Tongi/Uttara, reach out immediately:")
        st.markdown("""
            <div class='sched-card' style='border-left: 4px solid #EF4444;'>
                <b>Campus Security Control Room</b><br>
                📞 Hotline: +880 1713-393291<br>
                <span style='font-size: 0.75rem; color: #94A3B8;'>Available 24/7 for urgent assistance.</span>
            </div>
            <div class='sched-card' style='border-left: 4px solid #F59E0B;'>
                <b>Medical Center Emergency</b><br>
                📞 Ambulance: +880 1819-000000<br>
                <span style='font-size: 0.75rem; color: #94A3B8;'>First aid and emergency evacuation.</span>
            </div>
        """, unsafe_allow_html=True)
        if st.button("🚨 Trigger Panic Alert (Test)", type="primary", use_container_width=True):
            st.error("⚠️ Emergency alert sent to security desk with your GPS location!")

    elif st.session_state.active_tab == "Faculty":
        st.markdown("### 👨‍🏫 Faculty Directory")
        st.text_input("Search Faculty", placeholder="Search by name or department...")
        st.markdown("""
            <div class='sched-card'>
                <b>Prof. Dr. M. Ahmed</b><br>
                <span class='badge-tag'>EEE Department</span><br>
                📧 Email: m.ahmed@iubat.edu<br>
                🕒 Consultation: Sun-Tue (03:00 PM - 05:00 PM)
            </div>
            <div class='sched-card'>
                <b>Dr. Selim Reza</b><br>
                <span class='badge-tag'>ECE Department</span><br>
                📧 Email: selim.reza@iubat.edu<br>
                🕒 Consultation: Mon-Wed (11:00 AM - 01:00 PM)
            </div>
        """, unsafe_allow_html=True)

    elif st.session_state.active_tab == "Bus":
        st.markdown("### 🚌 Bus Schedule & Live Tracking")
        st.markdown("""
            <div class='sched-card'>
                <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;'>
                    <span style='font-weight: 700;'>Bus 02: Campus to Tongi</span>
                    <span class='badge-tag'>On Trip</span>
                </div>
                <div style='color: #94A3B8; font-size: 0.8rem; margin-bottom: 8px;'>
                    🕒 Departure: <b>05:30 PM</b> | ETA: <b>07:30 PM</b>
                </div>
                <div style='font-size: 0.8rem;'><b>Driver:</b> Sobuj Hossain (01621796157)</div>
                <div style='font-size: 0.8rem;'><b>Helper:</b> Ripon (01861455868)</div>
            </div>
        """, unsafe_allow_html=True)
        with st.expander("🗺️️ Route Stoppages"):
            st.markdown("""
                <div class='route-stop'>📍 Campus (Uttara)</div>
                <div class='route-stop'>📍 Tongi Station Road</div>
                <div class='route-stop'>📍 Amtoly Mor</div>
                <div class='route-stop'>📍 T & T Bazar</div>
                <div class='route-stop'>📍 Shilmoon</div>
                <div class='route-stop'>📍 Nimtoly Bridge</div>
            """, unsafe_allow_html=True)

    elif st.session_state.active_tab == "Alumni":
        st.markdown("### 🎓 Alumni Network & Mentorship")
        st.markdown("Connect with senior graduates working in top engineering firms globally and locally.")
        st.markdown("""
            <div class='sched-card'>
                <b>Tanvir Ahmed, P.Eng</b><br>
                <span class='badge-tag'>Class of 2021</span><br>
                💼 Senior Electrical Engineer at Energypac<br>
                🤝 Mentorship Focus: Power Systems & Substation Design
            </div>
            <div class='sched-card'>
                <b>Nusrat Jahan</b><br>
                <span class='badge-tag'>Class of 2023</span><br>
                💻 Software Engineer at BJIT<br>
                🤝 Mentorship Focus: Embedded C & Python
            </div>
        """, unsafe_allow_html=True)
