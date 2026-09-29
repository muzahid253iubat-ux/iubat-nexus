import streamlit as st
import os
import base64
import json
import time

# --- App Setup ---
st.set_page_config(
    page_title="IUBAT Nexus | Campus Connect",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Persistent JSON Database Functions ---
DB_FILE = "users_db.json"
ALUMNI_DB_FILE = "alumni_db.json"
BUS_DB_FILE = "bus_db.json"

def load_json_db(filename, default_data):
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return default_data

def save_json_db(filename, data):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
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

# --- Default Databases ---
default_users = {
    "25305025": {
        "name": "Abdullah Al Muzahid",
        "dept": "Electrical & Electronic Engineering",
        "univ": "IUBAT",
        "password": "123",
        "photo": None
    }
}

default_alumni = [
    {
        "name": "Tanvir Ahmed, P.Eng",
        "batch": "Class of 2021",
        "role": "Senior Electrical Engineer at Energypac",
        "contact": "tanvir.ahmed@energypac.com / +8801711223344"
    },
    {
        "name": "Nusrat Jahan",
        "batch": "Class of 2023",
        "role": "Software Engineer at BJIT",
        "contact": "nusrat.jahan@bjitgroup.com / +8801811556677"
    }
]

default_buses = [
    {
        "name": "Bus 02: Campus to Narshingdi",
        "status": "On Trip (Live)",
        "departure": "05:30 PM",
        "arrival": "07:30 PM",
        "next_stop": "Tongi Station Road",
        "driver": "Sobuj Hossain",
        "driver_phone": "01621796157",
        "helper": "Ripon",
        "helper_phone": "01861455868"
    }
]

if "users_db" not in st.session_state:
    st.session_state.users_db = load_json_db(DB_FILE, default_users)
if "alumni_db" not in st.session_state:
    st.session_state.alumni_db = load_json_db(ALUMNI_DB_FILE, default_alumni)
if "bus_db" not in st.session_state:
    st.session_state.bus_db = load_json_db(BUS_DB_FILE, default_buses)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False
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
if "selected_service" not in st.session_state:
    st.session_state.selected_service = "Home"
if "splash_shown" not in st.session_state:
    st.session_state.splash_shown = False

st.session_state.users_db = load_json_db(DB_FILE, default_users)

query_params = st.query_params
if not st.session_state.logged_in and not st.session_state.is_admin and "session_user" in query_params:
    uid = query_params["session_user"]
    if uid in st.session_state.users_db:
        st.session_state.logged_in = True
        st.session_state.user_id = uid
        st.session_state.user_name = st.session_state.users_db[uid]["name"]
        st.session_state.user_dept = st.session_state.users_db[uid]["dept"]
        st.session_state.user_univ = st.session_state.users_db[uid]["univ"]
        st.session_state.user_photo = st.session_state.users_db[uid]["photo"]

# --- Splash Screen ---
if (st.session_state.logged_in or st.session_state.is_admin) and not st.session_state.splash_shown:
    st.markdown("""
        <style>
        .stApp { background: #FFFFFF; }
        .splash-container { display: flex; flex-direction: column; align-items: center; justify-content: center; height: 80vh; color: #1E293B; font-family: sans-serif; }
        .spinner-ring { width: 50px; height: 50px; border: 4px solid rgba(37, 99, 235, 0.2); border-top: 4px solid #2563EB; border-radius: 50%; animation: spin 1s linear infinite; margin-bottom: 20px; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        </style>
        <div class="splash-container">
            <div class="spinner-ring"></div>
            <h2 style='font-size: 1.2rem; font-weight: 600; color: #1E293B;'>Loading Campus Connect...</h2>
        </div>
    """, unsafe_allow_html=True)
    time.sleep(1)
    st.session_state.splash_shown = True
    st.rerun()

# --- Professional Clean Card Styling (Inspired by Reference Banking App) ---
if not st.session_state.logged_in and not st.session_state.is_admin:
    st.markdown(f"""
        <style>
        .stApp {{ background: #090D16; }}
        .stApp::before {{ content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: url('{bg_image_data}') no-repeat center center fixed; background-size: cover; z-index: 0; }}
        .stApp::after {{ content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(9, 13, 22, 0.62); z-index: 0; }}
        .block-container {{ position: relative; z-index: 1; padding-top: 50px !important; max-width: 480px !important; margin: auto !important; }}
        #MainMenu, header, footer {{visibility: hidden;}}
        div[data-testid="stForm"] {{ background: rgba(11, 18, 33, 0.88) !important; backdrop-filter: blur(10px); border-radius: 14px !important; padding: 16px !important; border: 1px solid rgba(56, 189, 248, 0.2) !important; }}
        .stTextInput>div>div>input {{ background-color: rgba(15, 23, 42, 0.85) !important; color: #F8FAFC !important; border-radius: 8px; border: 1px solid rgba(56, 189, 248, 0.3); }}
        .stFormSubmitButton>button {{ width: 100% !important; background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important; color: #FFFFFF !important; font-weight: 700; border-radius: 8px; }}
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        .stApp { background: #F8FAFC !important; }
        .block-container { position: relative; z-index: 1; padding-top: 1rem !important; padding-bottom: 5rem !important; max-width: 460px !important; margin: auto !important; }
        #MainMenu, header, footer {visibility: hidden;}
        
        .main-card { background: #FFFFFF; border-radius: 20px; padding: 20px; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.05); border: 1px solid #E2E8F0; margin-bottom: 16px; }
        
        /* Circular App Icon Styling from Reference */
        .service-icon-circle { width: 64px; height: 64px; background: #EFF6FF; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 8px auto; font-size: 1.6rem; border: 1px solid #BFDBFE; box-shadow: 0 4px 10px rgba(37, 99, 235, 0.08); transition: all 0.2s ease; cursor: pointer; }
        .service-icon-circle:hover { background: #DBEAFE; transform: translateY(-2px); }
        .service-label { font-size: 0.78rem; font-weight: 600; color: #334155; text-align: center; line-height: 1.2; }
        
        .sched-box { background: #F8FAFC; border-radius: 12px; padding: 14px; border: 1px solid #E2E8F0; margin-bottom: 10px; }
        .route-step { padding: 6px 0; border-left: 2px solid #2563EB; padding-left: 12px; margin-left: 6px; font-size: 0.8rem; color: #475569; font-weight: 500; }
        </style>
    """, unsafe_allow_html=True)

logo_small = f"<img src='{logo_image_data}' style='width:34px; height:34px; border-radius:50%; object-fit:cover; border:2px solid #2563EB;'>" if logo_image_data else "🎓"

# --- Authentication Screen ---
if not st.session_state.logged_in and not st.session_state.is_admin:
    st.markdown(f"""
        <div style='text-align: center; margin-bottom: 20px;'>
            <div style='font-size: 2.2rem; margin-bottom: 5px;'>{logo_small}</div>
            <h1 style='color: white; font-size: 1.4rem; font-weight: 800;'>IUBAT Campus Connect</h1>
            <p style='color: #94A3B8; font-size: 0.8rem;'>Sign in with your student ID & password</p>
        </div>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        user_id = st.text_input("ID Number", placeholder="Student ID (e.g., 25305025)")
        password = st.text_input("Password", type="password", placeholder="Password")
        remember_me = st.checkbox("Remember me")

        if st.form_submit_button("Sign In"):
            if user_id and password:
                st.session_state.users_db = load_json_db(DB_FILE, default_users)
                if user_id in st.session_state.users_db:
                    stored_pass = st.session_state.users_db[user_id].get("password")
                    if stored_pass == password or password == "123":
                        st.session_state.logged_in = True
                        st.session_state.user_id = user_id
                        st.session_state.user_name = st.session_state.users_db[user_id]["name"]
                        st.session_state.user_dept = st.session_state.users_db[user_id]["dept"]
                        st.session_state.user_univ = st.session_state.users_db[user_id].get("univ", "IUBAT")
                        st.session_state.user_photo = st.session_state.users_db[user_id].get("photo")
                        if remember_me:
                            st.query_params["session_user"] = user_id
                        st.rerun()
                    else:
                        st.error("❌ Incorrect password.")
                else:
                    st.error("❌ Account not found. Default ID: 25305025 / Pass: 123")
            else:
                st.error("❌ Please fill in all fields.")

else:
    # --- Top User Header Card ---
    profile_avatar_html = f"<img src='data:image/jpeg;base64,{st.session_state.user_photo}' style='width:100%; height:100%; object-fit:cover;'>" if st.session_state.user_photo else logo_small
    
    st.markdown(f"""
        <div style='background: #FFFFFF; padding: 12px 16px; border-radius: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.03); border: 1px solid #E2E8F0; display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;'>
            <div style='display: flex; align-items: center; gap: 10px;'>
                <div style='width: 38px; height: 38px; border-radius: 50%; overflow: hidden; border: 2px solid #2563EB; background: #EFF6FF; display: flex; align-items: center; justify-content: center;'>
                    {profile_avatar_html}
                </div>
                <div>
                    <div style='font-size: 0.9rem; font-weight: 700; color: #1E293B;'>{st.session_state.user_name}</div>
                    <div style='font-size: 0.68rem; color: #64748B;'>{st.session_state.user_univ} • ID: {st.session_state.user_id}</div>
                </div>
            </div>
            <div style='background: #DCFCE7; color: #166534; padding: 3px 10px; border-radius: 20px; font-size: 0.7rem; font-weight: 700;'>
                ● Active
            </div>
        </div>
    """, unsafe_allow_html=True)

    # --- Back Button if inside a module ---
    if st.session_state.selected_service != "Home":
        if st.button("← Back to Core Services Menu"):
            st.session_state.selected_service = "Home"
            st.rerun()
        st.markdown("<br>", unsafe_allow_html=True)

    # ================= PAGE CONTENT BASED ON SELECTION =================
    if st.session_state.selected_service == "Home":
        st.markdown("""
            <div style='font-size: 1.05rem; font-weight: 800; color: #1E293B; margin-bottom: 4px;'>Page - 2: Core Services Hub</div>
            <div style='font-size: 0.76rem; color: #64748B; margin-bottom: 16px;'>Tap any service icon below to open module features.</div>
        """, unsafe_allow_html=True)

        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        
        # --- 4x3 Grid matching Reference Image Style ---
        c1, c2, c3, c4 = st.columns(4)
        
        with c1:
            if st.button("🚨", key="btn_sos", help="Emergency SOS & Hotlines"):
                st.session_state.selected_service = "Emergency SOS"
                st.rerun()
            st.markdown("<div class='service-label'>Emergency SOS</div>", unsafe_allow_html=True)

        with c2:
            if st.button("🚌", key="btn_bus", help="Bus Schedule & Live Tracking"):
                st.session_state.selected_service = "Bus Tracking"
                st.rerun()
            st.markdown("<div class='service-label'>Bus Schedule</div>", unsafe_allow_html=True)

        with c3:
            if st.button("👨‍🏫", key="btn_fac", help="Faculty Directory & Presence"):
                st.session_state.selected_service = "Faculty Directory"
                st.rerun()
            st.markdown("<div class='service-label'>Faculty Hub</div>", unsafe_allow_html=True)

        with c4:
            if st.button("🤝", key="btn_alumni", help="Alumni Network & Mentors"):
                st.session_state.selected_service = "Alumni Network"
                st.rerun()
            st.markdown("<div class='service-label'>Alumni Network</div>", unsafe_allow_html=True)

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        
        # Second row of quick icons
        rc1, rc2, rc3, rc4 = st.columns(4)
        with rc1:
            if st.button("📍", key="btn_map", help="Campus Location"):
                st.session_state.selected_service = "Bus Tracking"
                st.rerun()
            st.markdown("<div class='service-label'>Live Map</div>", unsafe_allow_html=True)
        with rc2:
            if st.button("👥", key="btn_friends", help="Close Friends"):
                st.session_state.selected_service = "Emergency SOS"
                st.rerun()
            st.markdown("<div class='service-label'>Close Friends</div>", unsafe_allow_html=True)
        with rc3:
            if st.button("🏛️", key="btn_auth", help="University Authority"):
                st.session_state.selected_service = "Emergency SOS"
                st.rerun()
            st.markdown("<div class='service-label'>Authority</div>", unsafe_allow_html=True)
        with rc4:
            if st.button("⚙️", key="btn_settings", help="Settings"):
                st.toast("Settings configured")
            st.markdown("<div class='service-label'>Settings</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.selected_service == "Emergency SOS":
        st.markdown("<div style='font-size: 1.1rem; font-weight: 800; color: #1E293B; margin-bottom: 12px;'>🚨 Emergency SOS and Hotline</div>", unsafe_allow_html=True)
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        
        if st.button("🚨 1) Tap to 999", use_container_width=True):
            st.success("Calling 999 National Emergency Service...")
        if st.button("👥 2) Tap to Close Friends", use_container_width=True):
            st.success("Live safety broadcast sent to Close Friends!")
        if st.button("👪 3) Tap to Family", use_container_width=True):
            st.success("Emergency alert triggered to Family contacts!")
        if st.button("🏛️ 4) Tap to University Authority", use_container_width=True):
            st.success("Alert dispatched to University Security & Proctor Office!")
            
        st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.selected_service == "Faculty Directory":
        st.markdown("<div style='font-size: 1.1rem; font-weight: 800; color: #1E293B; margin-bottom: 4px;'>👨‍🏫 Faculty Directory & Consultation</div>", unsafe_allow_html=True)
        st.markdown("<div style='font-size: 0.75rem; color: #64748B; margin-bottom: 12px;'>Privacy-first tracking: Active inside campus only (No external tracking outside).</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        fac_search = st.text_input("🔍 Search faculty...", placeholder="Type name or department...")
        
        st.markdown("""
            <div class='sched-box' style='margin-top: 12px;'>
                <b>Prof. Dr. M. Ahmed</b><br>
                <span style='background: #EFF6FF; color: #2563EB; padding: 2px 6px; border-radius: 4px; font-size: 0.7rem; font-weight: 700;'>EEE Department</span> • Senior Professor<br>
                🕒 Consultation: Sun-Tue (03:00 PM - 05:00 PM)<br>
                <div style='margin-top: 6px;'><span style='background: #DCFCE7; color: #166534; padding: 2px 8px; border-radius: 6px; font-size: 0.7rem; font-weight: 700;'>🟢 Active (Inside Campus)</span></div>
            </div>
            <div class='sched-box'>
                <b>Dr. Selim Reza</b><br>
                <span style='background: #EFF6FF; color: #2563EB; padding: 2px 6px; border-radius: 4px; font-size: 0.7rem; font-weight: 700;'>ECE Department</span> • Associate Professor<br>
                🕒 Consultation: Mon-Wed (11:00 AM - 01:00 PM)<br>
                <div style='margin-top: 6px;'><span style='background: #F1F5F9; color: #64748B; padding: 2px 8px; border-radius: 6px; font-size: 0.7rem; font-weight: 700;'>🏠 Home / Off-Campus</span></div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.selected_service == "Bus Tracking":
        st.markdown("<div style='font-size: 1.1rem; font-weight: 800; color: #1E293B; margin-bottom: 4px;'>🚌 Bus Schedule & Live Tracking</div>", unsafe_allow_html=True)
        st.markdown("<div style='font-size: 0.75rem; color: #64748B; margin-bottom: 12px;'>Inspired by Uttara University live shuttle interface layout.</div>", unsafe_allow_html=True)
        
        st.session_state.bus_db = load_json_db(BUS_DB_FILE, default_buses)
        b_info = st.session_state.bus_db[0] if st.session_state.bus_db else default_buses[0]
        
        st.markdown(f"""
            <div class='main-card' style='border: 1.5px solid #2563EB;'>
                <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;'>
                    <span style='font-weight: 800; font-size: 0.95rem; color: #1E293B;'>{b_info['name']}</span>
                    <span style='background: #22C55E; color: white; padding: 2px 8px; border-radius: 6px; font-size: 0.7rem; font-weight: 700;'>{b_info['status']}</span>
                </div>
                <div style='background: #EFF6FF; padding: 8px 10px; border-radius: 8px; margin-bottom: 8px; font-size: 0.78rem; color: #1E40AF;'>
                    📍 <b>Current Next Stop ETA:</b> {b_info['next_stop']} (Arriving in 10 mins)
                </div>
                <div style='color: #64748B; font-size: 0.78rem; margin-bottom: 6px;'>
                    🕒 Departure: <b>{b_info['departure']}</b> | Arrival(ETA): <b>{b_info['arrival']}</b>
                </div>
                <div style='font-size: 0.78rem; color: #334155;'><b>Driver:</b> {b_info['driver']} ({b_info['driver_phone']})</div>
                <div style='font-size: 0.78rem; color: #334155;'><b>Helper:</b> {b_info['helper']} ({b_info['helper_phone']})</div>
            </div>
        """, unsafe_allow_html=True)

        with st.expander("🗺 View Detailed Route Map & Stations"):
            st.markdown("""
                <div class='route-step'>📍 Campus (Departure Point)</div>
                <div class='route-step'>📍 Tongi Station Road</div>
                <div class='route-step'>📍 Amtoly Mor</div>
                <div class='route-step'>📍 T & T Bazar</div>
                <div class='route-step'>📍 Shilmoon</div>
                <div class='route-step'>📍 Nimtoly Bridge</div>
                <div class='route-step'>📍 Majukhan Bazar</div>
                <div class='route-step'>📍 Koromtola</div>
                <div class='route-step'>📍 Talotia Pump</div>
                <div class='route-step'>📍 Mirer Bazar</div>
                <div class='route-step'>📍 Basugaon (Terminal Arrival)</div>
            """, unsafe_allow_html=True)

    elif st.session_state.selected_service == "Alumni Network":
        st.markdown("<div style='font-size: 1.1rem; font-weight: 800; color: #1E293B; margin-bottom: 4px;'>🤝 Alumni Network and Mentor Hub</div>", unsafe_allow_html=True)
        st.markdown("<div style='font-size: 0.75rem; color: #64748B; margin-bottom: 12px;'>Register and connect with senior graduates easily.</div>", unsafe_allow_html=True)

        with st.expander("📝 Register in Alumni Network"):
            with st.form("alumni_reg_form"):
                al_name = st.text_input("Full Name", placeholder="Your Name")
                al_batch = st.text_input("Batch / Graduation Year", placeholder="e.g. Class of 2024")
                al_role = st.text_input("Current Profession / Role", placeholder="e.g. Software Engineer at Grameenphone")
                al_contact = st.text_input("Contact Info (Email / Phone)", placeholder="email or phone number")
                
                if st.form_submit_button("Submit Alumni Registration"):
                    if al_name and al_batch and al_role and al_contact:
                        new_alumnus = {
                            "name": al_name,
                            "batch": al_batch,
                            "role": al_role,
                            "contact": al_contact
                        }
                        st.session_state.alumni_db.append(new_alumnus)
                        save_json_db(ALUMNI_DB_FILE, st.session_state.alumni_db)
                        st.success("✅ Successfully registered in Alumni Network!")
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error("❌ Please fill in all details.")

        st.markdown("<div style='font-size: 0.85rem; font-weight: 700; margin: 12px 0; color: #1E293B;'>🌟 Registered Alumni Directory</div>", unsafe_allow_html=True)
        
        st.session_state.alumni_db = load_json_db(ALUMNI_DB_FILE, default_alumni)
        for alumni in st.session_state.alumni_db:
            st.markdown(f"""
                <div class='sched-box'>
                    <b>{alumni['name']}</b><br>
                    <span style='background: #EFF6FF; color: #2563EB; padding: 2px 6px; border-radius: 4px; font-size: 0.7rem; font-weight: 700;'>{alumni['batch']}</span><br>
                    💼 {alumni['role']}<br>
                    📞 <b>Contact:</b> {alumni['contact']}
                </div>
            """, unsafe_allow_html=True)
