import streamlit as st
import os
import base64
import time

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

# --- Persistent Session Management ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_id" not in st.session_state:
    st.session_state.user_id = ""
if "user_name" not in st.session_state:
    st.session_state.user_name = "Abdullah Al Muzahid"
if "user_dept" not in st.session_state:
    st.session_state.user_dept = "Electrical & Electronic Engineering"
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Home"
if "is_registering" not in st.session_state:
    st.session_state.is_registering = False
if "splash_shown" not in st.session_state:
    st.session_state.splash_shown = False

query_params = st.query_params
if not st.session_state.logged_in and "session_user" in query_params:
    st.session_state.logged_in = True
    st.session_state.user_id = query_params["session_user"]

# --- 1-Second Splash Screen Logic for Logged-In Users ---
if st.session_state.logged_in and not st.session_state.splash_shown:
    st.markdown("""
        <style>
        .stApp { background: #090D16; }
        .splash-container {
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            height: 80vh; color: white; font-family: sans-serif;
        }
        .spinner-ring {
            width: 50px; height: 50px; border: 4px solid rgba(56, 189, 248, 0.2);
            border-top: 4px solid #38BDF8; border-radius: 50%;
            animation: spin 1s linear infinite; margin-bottom: 20px;
        }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        </style>
        <div class="splash-container">
            <div class="spinner-ring"></div>
            <h2 style='font-size: 1.2rem; font-weight: 600; color: #F8FAFC;'>Loading IUBAT Nexus...</h2>
        </div>
    """, unsafe_allow_html=True)
    time.sleep(1)
    st.session_state.splash_shown = True
    st.rerun()

# --- Dynamic Styling & Layout ---
if not st.session_state.logged_in:
    st.markdown(f"""
        <style>
        .stApp {{ background: #090D16; }}
        .stApp::before {{
            content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: url('{bg_image_data}') no-repeat center center fixed; background-size: cover; z-index: 0;
        }}
        .stApp::after {{
            content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(9, 13, 22, 0.78); z-index: 0;
        }}
        .block-container {{
            position: relative; z-index: 1; padding-top: 1.2rem !important; max-width: 520px !important; margin: auto !important;
        }}
        #MainMenu, header, footer {{visibility: hidden;}}

        /* Perfect Header Layout for Left & Right Corner */
        .top-navbar {{
            display: flex; justify-content: space-between; align-items: center;
            margin-bottom: 25px; width: 100%; gap: 10px; flex-wrap: wrap;
        }}
        .nav-brand {{
            display: flex; align-items: center; gap: 10px; color: #FFFFFF; font-weight: 700; font-size: 1.1rem;
        }}
        .nav-brand img {{ width: 36px; height: 36px; border-radius: 50%; object-fit: cover; border: 1.5px solid #38BDF8; }}
        
        .nav-actions {{ display: flex; align-items: center; gap: 8px; }}

        /* Custom Streamlit Button Styling for Full Text Display */
        .stButton>button {{
            background: rgba(30, 41, 59, 0.85) !important;
            color: #F8FAFC !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 8px !important;
            font-size: 0.78rem !important;
            font-weight: 600 !important;
            padding: 6px 12px !important;
            white-space: nowrap !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            transition: all 0.2s ease;
        }}
        .stButton>button:hover {{
            background: rgba(51, 65, 85, 0.95) !important;
            border-color: #38BDF8 !important;
            color: #38BDF8 !important;
        }}
        
        /* Hero Section */
        .hero-showcase {{
            display: flex; justify-content: center; align-items: center; gap: 14px; margin-bottom: 18px;
        }}
        .floating-badge {{
            width: 40px; height: 40px; background: rgba(30, 41, 59, 0.85); border-radius: 50%;
            display: flex; align-items: center; justify-content: center; box-shadow: 0 8px 20px rgba(0,0,0,0.4);
            border: 1px solid rgba(255,255,255,0.15); font-size: 1rem; animation: float 3s ease-in-out infinite;
        }}
        .floating-badge:nth-child(even) {{ animation-delay: 1.5s; }}
        @keyframes float {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-5px); }} }}

        .central-avatar {{
            width: 75px; height: 75px; background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
            border-radius: 50%; display: flex; align-items: center; justify-content: center;
            box-shadow: 0 10px 30px rgba(37, 99, 235, 0.4); border: 2.5px solid rgba(56, 189, 248, 0.6); overflow: hidden;
        }}
        .central-avatar img {{ width: 100%; height: 100%; object-fit: cover; }}

        .hero-title {{
            text-align: center; color: #F8FAFC !important; font-size: 1.7rem; font-weight: 800; line-height: 1.2; margin-bottom: 8px;
        }}
        .hero-subtitle {{
            text-align: center; color: #94A3B8 !important; font-size: 0.8rem; line-height: 1.4; margin-bottom: 22px; padding: 0 10px;
        }}

        div[data-testid="stForm"] {{
            background: rgba(15, 23, 42, 0.9) !important; backdrop-filter: blur(16px);
            border-radius: 18px !important; padding: 20px 18px 16px 18px !important;
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.7) !important; border: 1px solid rgba(255, 255, 255, 0.12) !important;
        }}
        div[data-testid="stTextInput"] label {{ display: none !important; }}
        .stTextInput>div>div>input {{
            background-color: rgba(30, 41, 59, 0.8) !important; color: #F8FAFC !important; border-radius: 8px;
            border: 1.5px solid rgba(255, 255, 255, 0.12); padding: 9px 12px; font-size: 0.85rem;
        }}
        .stFormSubmitButton>button {{
            width: 100% !important; background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
            color: #FFFFFF !important; font-weight: 700; border-radius: 8px; border: none; padding: 10px;
        }}
        </style>
    """, unsafe_allow_html=True)

else:
    st.markdown("""
        <style>
        .stApp { background: #0F172A !important; }
        .block-container { position: relative; z-index: 1; padding-top: 1.5rem !important; padding-bottom: 2rem !important; max-width: 420px !important; margin: auto !important; }
        #MainMenu, header, footer {visibility: hidden;}

        .app-header {
            background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(10px); padding: 14px 18px;
            border-radius: 16px; color: white; margin-bottom: 16px; border: 1px solid rgba(255,255,255,0.08);
            display: flex; justify-content: space-between; align-items: center;
        }
        .sched-card {
            background: rgba(30, 41, 59, 0.75); border-radius: 14px; padding: 14px; color: #F8FAFC;
            border: 1px solid rgba(255,255,255,0.1); margin-bottom: 10px;
        }
        .badge-tag {
            background: rgba(56, 189, 248, 0.15); color: #38BDF8; padding: 3px 8px; border-radius: 6px; font-size: 0.7rem; font-weight: 600;
        }
        .route-stop {
            padding: 6px 0; border-left: 2px solid #38BDF8; padding-left: 12px; margin-left: 6px; font-size: 0.8rem; color: #CBD5E1;
        }
        </style>
    """, unsafe_allow_html=True)


# --- UI Render Logic ---
avatar_html = f"<div class='central-avatar'><img src='{logo_image_data}' alt='Logo'></div>" if logo_image_data else "<div class='central-avatar'>🎓</div>"
logo_small = f"<img src='{logo_image_data}' alt='Logo'>" if logo_image_data else "🎓"

if not st.session_state.logged_in:
    # Top Navbar: Left corner brand, Right corner full text buttons
    col_left, col_right1, col_right2 = st.columns([1.5, 1.1, 1.1])
    
    with col_left:
        st.markdown(f"""
            <div class="nav-brand">
                {logo_small} IUBAT Nexus
            </div>
        """, unsafe_allow_html=True)
        
    with col_right1:
        if st.button("Create an account", use_container_width=True):
            st.session_state.is_registering = True
            st.rerun()
            
    with col_right2:
        if st.button("Go to Account", use_container_width=True):
            st.session_state.is_registering = False
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    if st.session_state.is_registering:
        # --- Register View ---
        st.markdown("""
            <div class="hero-title" style="font-size: 1.5rem; margin-top: 10px;">Create your IUBAT Account</div>
            <div class="hero-subtitle">Access campus services, academic tools, and student portals instantly.</div>
        """, unsafe_allow_html=True)

        with st.form("register_form"):
            reg_name = st.text_input("Full Name", placeholder="Full Name *")
            reg_id = st.text_input("ID Number", placeholder="Student ID Number *")
            reg_dept = st.text_input("Department", placeholder="e.g. Electrical & Electronic Engineering")
            reg_pass = st.text_input("Password", type="password", placeholder="Create Password *")

            if st.form_submit_button("Complete Registration & Sign In"):
                if reg_name and reg_id and reg_pass:
                    st.session_state.logged_in = True
                    st.session_state.user_id = reg_id
                    st.session_state.user_name = reg_name
                    if reg_dept:
                        st.session_state.user_dept = reg_dept
                    st.session_state.active_tab = "Home"
                    st.query_params["session_user"] = reg_id
                    st.rerun()
                else:
                    st.error("❌ Please fill in all required fields.")
        
        if st.button("⬅️ Already have an account? Sign In", use_container_width=True):
            st.session_state.is_registering = False
            st.rerun()

    else:
        # --- Login View ---
        st.markdown(f"""
            <div class="hero-showcase" style="margin-top: 10px;">
                <div class="floating-badge">🚨</div>
                <div class="floating-badge">👨‍🏫</div>
                {avatar_html}
                <div class="floating-badge">🚌</div>
                <div class="floating-badge">🎓</div>
            </div>
            <div class="hero-title">All of IUBAT,<br>working for you</div>
            <div class="hero-subtitle">Sign in to your Student Portal for seamless access to campus services and academic records.</div>
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

    st.markdown("<div style='text-align: center; color: #94A3B8; font-size: 11px; margin-top: 15px;'>© 2026 IUBAT Nexus • Secure Portal</div>", unsafe_allow_html=True)

else:
    # --- Main Logged-In Dashboard ---
    st.markdown(f"""
        <div class='app-header'>
            <div>
                <div style='font-size: 0.7rem; color: #94A3B8;'>Welcome back,</div>
                <div style='font-size: 1.05rem; font-weight: 800; color: #F8FAFC;'>{st.session_state.user_name}</div>
                <div style='font-size: 0.7rem; color: #38BDF8;'>ID: {st.session_state.user_id}</div>
            </div>
            <div>
                <span class='badge-tag'>🟢 Online</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Top Tab Navigation inside Dashboard (includes Go to Account button for updating info)
    col_t1, col_t2, col_t3 = st.columns(3)
    with col_t1:
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.active_tab = "Home"
            st.rerun()
    with col_t2:
        if st.button("⚙️ Go to Account", use_container_width=True):
            st.session_state.active_tab = "Account"
            st.rerun()
    with col_t3:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.splash_shown = False
            st.session_state.active_tab = "Home"
            if "session_user" in st.query_params:
                del st.query_params["session_user"]
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

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

    elif st.session_state.active_tab == "Account":
        st.markdown("### ⚙️ Account Management")
        st.markdown("Update your student profile information anytime below:")
        
        with st.form("update_account_form"):
            new_name = st.text_input("Full Name", value=st.session_state.user_name)
            new_dept = st.text_input("Department", value=st.session_state.user_dept)
            
            if st.form_submit_button("Save Changes"):
                st.session_state.user_name = new_name
                st.session_state.user_dept = new_dept
                st.success("✅ Account updated successfully!")
                time.sleep(0.5)
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
        with st.expander("🗺 Route Stoppages"):
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
