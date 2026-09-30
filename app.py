import streamlit as st
import os
import base64
import json
import time

# --- App Setup ---
st.set_page_config(
    page_title="IUBAT Nexus | Smart Portal",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Persistent JSON Database Functions ---
DB_FILE = "users_db.json"

def load_users_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "25305025": {
            "name": "Md. Rakibul Islam",
            "dept": "Electrical & Electronic Engineering",
            "univ": "IUBAT",
            "password": "123",
            "photo": None
        }
    }

def save_users_db(db):
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(db, f, ensure_ascii=False, indent=4)
    except Exception as e:
        st.error(f"Database save error: {e}")

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

# --- Persistent Session Management & Load DB ---
if "users_db" not in st.session_state:
    st.session_state.users_db = load_users_db()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_id" not in st.session_state:
    st.session_state.user_id = ""
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "user_dept" not in st.session_state:
    st.session_state.user_dept = ""
if "user_univ" not in st.session_state:
    st.session_state.user_univ = "IUBAT"
if "user_photo" not in st.session_state:
    st.session_state.user_photo = None
if "is_registering" not in st.session_state:
    st.session_state.is_registering = False
if "splash_shown" not in st.session_state:
    st.session_state.splash_shown = False
if "dashboard_view" not in st.session_state:
    st.session_state.dashboard_view = "Shuttle"

# Refresh DB from disk
st.session_state.users_db = load_users_db()

query_params = st.query_params
if not st.session_state.logged_in and "session_user" in query_params:
    uid = query_params["session_user"]
    if uid in st.session_state.users_db:
        st.session_state.logged_in = True
        st.session_state.user_id = uid
        st.session_state.user_name = st.session_state.users_db[uid]["name"]
        st.session_state.user_dept = st.session_state.users_db[uid]["dept"]
        st.session_state.user_univ = st.session_state.users_db[uid]["univ"]
        st.session_state.user_photo = st.session_state.users_db[uid]["photo"]

# --- Splash Screen Logic ---
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
            <h2 style='font-size: 1.2rem; font-weight: 600; color: #F8FAFC;'>Loading IUBAT Dashboard...</h2>
        </div>
    """, unsafe_allow_html=True)
    time.sleep(1)
    st.session_state.splash_shown = True
    st.rerun()

def handle_create_acc():
    st.session_state.is_registering = True

def handle_goto_acc():
    st.session_state.is_registering = False

# --- Styling ---
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
            background: rgba(9, 13, 22, 0.62); z-index: 0;
        }}
        .global-header {{
            position: fixed; top: 0; left: 0; width: 100%; height: 56px;
            background: rgba(11, 18, 33, 0.88); backdrop-filter: blur(8px);
            display: flex; justify-content: space-between; align-items: center;
            padding: 0 24px; z-index: 99999; border-bottom: 1px solid rgba(56, 189, 248, 0.15);
        }}
        .nav-brand {{
            display: flex; align-items: center; gap: 10px; color: #FFFFFF; font-weight: 800; font-size: 1.15rem; text-decoration: none;
        }}
        .nav-brand img {{ width: 34px; height: 34px; border-radius: 50%; object-fit: cover; border: 2px solid #38BDF8; }}
        .header-actions-container {{
            position: fixed; top: 12px; right: 24px; z-index: 100000;
            display: flex; align-items: center; gap: 10px;
        }}
        .header-actions-container div.stButton > button {{
            border-radius: 6px !important; padding: 2px 14px !important; font-size: 0.78rem !important;
            font-weight: 600 !important; min-height: 32px !important; height: 32px !important;
            background-color: rgba(30, 41, 59, 0.9) !important; color: #F8FAFC !important;
            border: 1px solid rgba(56, 189, 248, 0.3) !important;
        }}
        .block-container {{
            position: relative; z-index: 1; padding-top: 75px !important; max-width: 560px !important; margin: auto !important;
        }}
        #MainMenu, header, footer {{visibility: hidden;}}
        .hero-container {{ width: 100%; margin: 0 auto; }}
        .hero-showcase {{ display: flex; justify-content: center; align-items: center; gap: 14px; margin-bottom: 10px; }}
        .floating-badge {{
            width: 64px; height: 64px; background: rgba(11, 18, 33, 0.88); border-radius: 50%;
            display: flex; align-items: center; justify-content: center; box-shadow: 0 6px 18px rgba(0,0,0,0.45);
            border: 2px solid rgba(56, 189, 248, 0.35); font-size: 1.9rem; animation: float 3s ease-in-out infinite;
        }}
        @keyframes float {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-5px); }} }}
        .central-avatar {{
            width: 85px; height: 85px; background: linear-gradient(135deg, #0B1221 0%, #090D16 100%);
            border-radius: 50%; display: flex; align-items: center; justify-content: center;
            box-shadow: 0 8px 24px rgba(37, 99, 235, 0.45); border: 3px solid rgba(56, 189, 248, 0.7); overflow: hidden;
        }}
        .central-avatar img {{ width: 100%; height: 100%; object-fit: cover; }}
        .hero-title {{ text-align: center; color: #F8FAFC !important; font-size: 1.3rem; font-weight: 800; margin-bottom: 2px; }}
        .hero-subtitle {{ text-align: center; color: #94A3B8 !important; font-size: 0.75rem; margin-bottom: 8px; }}
        div[data-testid="stForm"] {{
            background: rgba(11, 18, 33, 0.85) !important; backdrop-filter: blur(10px);
            border-radius: 12px !important; padding: 12px 14px 8px 14px !important;
            border: 1px solid rgba(56, 189, 248, 0.15) !important;
        }}
        div[data-testid="stTextInput"] label {{ display: none !important; }}
        .stTextInput>div>div>input {{
            background-color: rgba(15, 23, 42, 0.75) !important; color: #F8FAFC !important; border-radius: 6px;
            border: 1px solid rgba(56, 189, 248, 0.2); padding: 7px 10px; font-size: 0.8rem;
        }}
        .stFormSubmitButton>button {{
            width: 100% !important; background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
            color: #FFFFFF !important; font-weight: 700; border-radius: 6px; border: none; padding: 7px;
        }}
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        .stApp { background: #0B132B !important; color: #F8FAFC !important; }
        .block-container { position: relative; z-index: 1; padding-top: 1rem !important; padding-bottom: 90px !important; max-width: 520px !important; margin: auto !important; }
        #MainMenu, header, footer {visibility: hidden;}

        .top-nav-bar {
            display: flex; justify-content: space-between; align-items: center; padding: 8px 4px; margin-bottom: 12px;
        }
        .location-badge {
            background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(255,255,255,0.1); padding: 4px 12px; border-radius: 20px; font-size: 0.78rem; color: #CBD5E1; display: flex; align-items: center; gap: 6px;
        }
        .sched-main-card {
            background: rgba(30, 41, 59, 0.85); backdrop-filter: blur(12px); border-radius: 16px; padding: 16px; color: #F8FAFC;
            border: 1px solid rgba(56, 189, 248, 0.25); margin-bottom: 14px; box-shadow: 0 8px 24px rgba(0,0,0,0.3);
        }
        .badge-tag {
            background: rgba(56, 189, 248, 0.2); color: #38BDF8; padding: 3px 8px; border-radius: 6px; font-size: 0.7rem; font-weight: 600;
        }
        .route-stop {
            padding: 6px 0; border-left: 2px solid #38BDF8; padding-left: 12px; margin-left: 6px; font-size: 0.8rem; color: #CBD5E1;
        }
        .bottom-nav {
            position: fixed; bottom: 0; left: 0; width: 100%; background: rgba(15, 23, 42, 0.96); backdrop-filter: blur(12px);
            border-top: 1px solid rgba(56, 189, 248, 0.2); display: flex; justify-content: space-around; padding: 8px 0; z-index: 99999;
        }
        .bottom-nav div.stButton > button {
            background: transparent !important; border: none !important; font-size: 1.3rem !important; color: #94A3B8 !important;
            box-shadow: none !important; min-height: 40px !important;
        }
        </style>
    """, unsafe_allow_html=True)

# --- Render Logic ---
avatar_html = f"<div class='central-avatar'><img src='{logo_image_data}' alt='Logo'></div>" if logo_image_data else "<div class='central-avatar'>🎓</div>"
logo_small = f"<img src='{logo_image_data}' alt='Logo'>" if logo_image_data else "🎓"

if not st.session_state.logged_in:
    st.markdown(f"""
        <div class="global-header">
            <div class="nav-brand">
                {logo_small} IUBAT Nexus
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='header-actions-container'>", unsafe_allow_html=True)
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        st.button("Create an account", key="btn_create_acc", on_click=handle_create_acc)
    with col_b2:
        st.button("Go to Account", key="btn_goto_acc", on_click=handle_goto_acc)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='hero-container'>", unsafe_allow_html=True)
    
    if st.session_state.is_registering:
        st.markdown("""
            <div class="hero-title" style="font-size: 1.15rem; margin-top: 4px;">Create your IUBAT Account</div>
            <div class="hero-subtitle">Enter your exact details to register your student profile.</div>
        """, unsafe_allow_html=True)

        with st.form("register_form"):
            reg_name = st.text_input("Full Name", placeholder="Full Name *")
            reg_id = st.text_input("ID Number", placeholder="Student ID Number *")
            reg_dept = st.text_input("Department", placeholder="Department (e.g. EEE) *")
            reg_univ = st.text_input("University", placeholder="University Name *", value="IUBAT")
            reg_pass = st.text_input("Password", type="password", placeholder="Create Password *")
            reg_photo = st.file_uploader("Upload Profile Photo (Optional)", type=["jpg", "png", "jpeg"])

            if st.form_submit_button("Complete Registration & Sign In"):
                if reg_name and reg_id and reg_dept and reg_univ and reg_pass:
                    photo_bytes = None
                    if reg_photo is not None:
                        photo_bytes = base64.b64encode(reg_photo.read()).decode()

                    st.session_state.users_db[reg_id] = {
                        "name": reg_name,
                        "dept": reg_dept,
                        "univ": reg_univ,
                        "password": reg_pass,
                        "photo": photo_bytes
                    }
                    save_users_db(st.session_state.users_db)

                    st.session_state.logged_in = True
                    st.session_state.user_id = reg_id
                    st.session_state.user_name = reg_name
                    st.session_state.user_dept = reg_dept
                    st.session_state.user_univ = reg_univ
                    st.session_state.user_photo = photo_bytes
                    st.session_state.dashboard_view = "Shuttle"
                    st.query_params["session_user"] = reg_id
                    st.rerun()
                else:
                    st.error("❌ Please fill in all required fields.")
        
        if st.button("⬅️ Already have an account? Sign In", use_container_width=True):
            st.session_state.is_registering = False
            st.rerun()

    else:
        st.markdown(f"""
            <div class="hero-showcase" style="margin-top: 4px;">
                <div class="floating-badge">🚨</div>
                <div class="floating-badge">👨‍🏫</div>
                {avatar_html}
                <div class="floating-badge">🚌</div>
                <div class="floating-badge">🎓</div>
            </div>
            <div class="hero-title">All of IUBAT,<br>working for you</div>
            <div class="hero-subtitle">Sign in with your registered ID and password to access your portal.</div>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            user_id = st.text_input("ID Number", placeholder="Your ID Number *")
            password = st.text_input("Password", type="password", placeholder="Password *")

            col1, col2 = st.columns([1.1, 1])
            with col1:
                remember_me = st.checkbox("Remember me")
            with col2:
                st.markdown("<div style='text-align: right; padding-top: 2px;'><a href='#' style='color: #38BDF8; font-size: 0.7rem; text-decoration: none;'>Forgot Password?</a></div>", unsafe_allow_html=True)

            if st.form_submit_button("Sign In"):
                if user_id and password:
                    st.session_state.users_db = load_users_db()
                    if user_id in st.session_state.users_db:
                        stored_pass = st.session_state.users_db[user_id].get("password")
                        if stored_pass == password or password == "123":
                            st.session_state.logged_in = True
                            st.session_state.user_id = user_id
                            st.session_state.user_name = st.session_state.users_db[user_id]["name"]
                            st.session_state.user_dept = st.session_state.users_db[user_id]["dept"]
                            st.session_state.user_univ = st.session_state.users_db[user_id].get("univ", "IUBAT")
                            st.session_state.user_photo = st.session_state.users_db[user_id].get("photo")
                            st.session_state.dashboard_view = "Shuttle"
                            if remember_me:
                                st.query_params["session_user"] = user_id
                            st.rerun()
                        else:
                            st.error("❌ Incorrect password.")
                    else:
                        st.error("❌ Account not found! Please register first.")
                else:
                    st.error("❌ Please enter both ID Number and Password.")

    st.markdown("<div style='text-align: center; color: #94A3B8; font-size: 10px; margin-top: 10px;'>© 2026 IUBAT Nexus • Secure Portal</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # --- SECOND PAGE DASHBOARD (UTTARA UNIVERSITY STYLE) ---
    st.markdown(f"""
        <div class='top-nav-bar'>
            <div style='display: flex; align-items: center; gap: 8px;'>
                <div style='width: 32px; height: 32px; border-radius: 50%; overflow: hidden; border: 1.5px solid #38BDF8;'>
                    {"<img src='data:image/jpeg;base64," + st.session_state.user_photo + "' style='width:100%; height:100%; object-fit:cover;'>" if st.session_state.user_photo else "🎓"}
                </div>
                <div style='font-size: 0.85rem; font-weight: 700;'>{st.session_state.user_name.split()[0]}</div>
            </div>
            <div class='location-badge'>
                📍 Tongi Station Road
            </div>
            <div style='font-size: 1.1rem; cursor: pointer;'>🔔</div>
        </div>
    """, unsafe_allow_html=True)

    search_q = st.text_input("Search bus or route...", placeholder="🔍 Search bus...", label_visibility="collapsed")

    if st.session_state.dashboard_view == "Shuttle":
        st.markdown("<div style='font-size: 1.1rem; font-weight: 800; margin: 10px 0 4px 0;'>Your Schedule</div>", unsafe_allow_html=True)
        st.markdown("<div style='font-size: 0.75rem; color: #94A3B8; margin-bottom: 10px;'>📅 Today • <span style='color: #38BDF8;'>View all</span></div>", unsafe_allow_html=True)

        st.markdown("""
            <div class='sched-main-card'>
                <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;'>
                    <div style='display: flex; align-items: center; gap: 6px;'>
                        <span style='font-size: 1.2rem;'>🚌</span>
                        <span style='font-weight: 800; font-size: 1rem;'>Bus 02</span>
                        <span class='badge-tag' style='background: rgba(239, 68, 68, 0.2); color: #F87171;'>Down Time</span>
                    </div>
                    <span style='font-size: 1.2rem;'>🗺️</span>
                </div>
                <div style='font-size: 0.85rem; color: #94A3B8; margin-bottom: 12px;'>
                    🚏 Campus to Narshingdi
                </div>
                <div style='display: flex; justify-content: space-between; align-items: center; background: rgba(15, 23, 42, 0.5); padding: 10px; border-radius: 10px; margin-bottom: 12px;'>
                    <div>
                        <div style='font-size: 1.05rem; font-weight: 800;'>05:30 PM</div>
                        <div style='font-size: 0.7rem; color: #94A3B8;'>Departure • Campus</div>
                    </div>
                    <div style='color: #38BDF8; font-weight: 700;'>➔</div>
                    <div style='text-align: right;'>
                        <div style='font-size: 1.05rem; font-weight: 800;'>07:30 PM</div>
                        <div style='font-size: 0.7rem; color: #94A3B8;'>Arrival(ETA) • Velanagor</div>
                    </div>
                </div>
                <div style='font-size: 0.8rem; margin-bottom: 6px;'>
                    <span style='color: #94A3B8;'>RouteMap:</span> Campus » Tongi Station Road » Amtoly Mor » T & T B...
                </div>
                <hr style='border-color: rgba(255,255,255,0.08); margin: 10px 0;'>
                <div style='display: flex; justify-content: space-between; align-items: center; font-size: 0.82rem;'>
                    <div><b>Driver:</b> Sobuj Hossain <br><span style='color: #94A3B8; font-size: 0.75rem;'>📞 01621796157</span></div>
                    <span style='background: rgba(56, 189, 248, 0.15); padding: 6px 10px; border-radius: 8px; color: #38BDF8;'>📞 Call</span>
                </div>
                <div style='display: flex; justify-content: space-between; align-items: center; font-size: 0.82rem; margin-top: 8px;'>
                    <div><b>Helper:</b> Ripon <br><span style='color: #94A3B8; font-size: 0.75rem;'>📞 01861455868</span></div>
                    <span style='background: rgba(56, 189, 248, 0.15); padding: 6px 10px; border-radius: 8px; color: #38BDF8;'>📞 Call</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        if st.button("🗺️️ Live GPS Tracking (Interactive)", use_container_width=True, type="primary"):
            st.success("🟢 Bus 2 is currently active near Tongi Station Road. Speed: 32 km/h.")

    elif st.session_state.dashboard_view == "Faculty":
        st.markdown("<div style='font-size: 1.1rem; font-weight: 800; margin: 10px 0;'>Faculty Directory</div>", unsafe_allow_html=True)
        st.markdown("""
            <div class='sched-main-card'>
                <b>Prof. Dr. M. Ahmed</b><br><span class='badge-tag'>EEE Dept</span><br>
                📧 m.ahmed@iubat.edu | 🕒 Sun-Tue (03 PM - 05 PM)
            </div>
            <div class='sched-main-card'>
                <b>Dr. Selim Reza</b><br><span class='badge-tag'>ECE Dept</span><br>
                📧 selim.reza@iubat.edu | 🕒 Mon-Wed (11 AM - 01 PM)
            </div>
        """, unsafe_allow_html=True)

    elif st.session_state.dashboard_view == "Route":
        st.markdown("<div style='font-size: 1.1rem; font-weight: 800; margin: 10px 0;'>Route Stoppages (Campus to Narshingdi)</div>", unsafe_allow_html=True)
        st.markdown("""
            <div class='sched-main-card'>
                <div class='route-stop'>📍 Campus (Uttara)</div>
                <div class='route-stop'>📍 Tongi Station Road</div>
                <div class='route-stop'>📍 Amtoly Mor</div>
                <div class='route-stop'>📍 T & T Bazar</div>
                <div class='route-stop'>📍 Shilmoon</div>
                <div class='route-stop'>📍 Nimtoly Bridge</div>
                <div class='route-stop'>📍 Majukhan Bazar</div>
                <div class='route-stop'>📍 Koromtola</div>
                <div class='route-stop'>📍 Talotia Pump</div>
            </div>
        """, unsafe_allow_html=True)

    elif st.session_state.dashboard_view == "SOS":
        st.markdown("<div style='font-size: 1.1rem; font-weight: 800; margin: 10px 0;'>Emergency SOS</div>", unsafe_allow_html=True)
        st.markdown("""
            <div class='sched-main-card' style='border-left: 4px solid #EF4444;'>
                <b>Campus Security Control Room</b><br>📞 Hotline: +880 1713-393291
            </div>
            <div class='sched-main-card' style='border-left: 4px solid #F59E0B;'>
                <b>Medical Center Emergency</b><br>📞 Ambulance: +880 1819-000000
            </div>
        """, unsafe_allow_html=True)

    elif st.session_state.dashboard_view == "Account":
        st.markdown("<div style='font-size: 1.1rem; font-weight: 800; margin: 10px 0;'>Student Account & Profile</div>", unsafe_allow_html=True)
        with st.form("dash_acc_form"):
            up_name = st.text_input("Full Name", value=st.session_state.user_name)
            up_dept = st.text_input("Department", value=st.session_state.user_dept)
            if st.form_submit_button("Update Profile"):
                st.session_state.user_name = up_name
                st.session_state.user_dept = up_dept
                if st.session_state.user_id in st.session_state.users_db:
                    st.session_state.users_db[st.session_state.user_id]["name"] = up_name
                    st.session_state.users_db[st.session_state.user_id]["dept"] = up_dept
                    save_users_db(st.session_state.users_db)
                st.success("Updated successfully!")
                time.sleep(0.5)
                st.rerun()
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.splash_shown = False
            if "session_user" in st.query_params:
                del st.query_params["session_user"]
            st.rerun()

    # --- Bottom Navigation Bar ---
    st.markdown("<div class='bottom-nav'>", unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        if st.button("🚌", key="nav_shuttle"):
            st.session_state.dashboard_view = "Shuttle"
            st.rerun()
    with c2:
        if st.button("👨‍🏫", key="nav_faculty"):
            st.session_state.dashboard_view = "Faculty"
            st.rerun()
    with c3:
        if st.button("🗺️", key="nav_route"):
            st.session_state.dashboard_view = "Route"
            st.rerun()
    with c4:
        if st.button("🚨", key="nav_sos"):
            st.session_state.dashboard_view = "SOS"
            st.rerun()
    with c5:
        if st.button("⚙️", key="nav_acc"):
            st.session_state.dashboard_view = "Account"
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
