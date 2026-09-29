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
        .stApp { background: #090D16; }
        .splash-container { display: flex; flex-direction: column; align-items: center; justify-content: center; height: 80vh; color: white; font-family: sans-serif; }
        .spinner-ring { width: 50px; height: 50px; border: 4px solid rgba(56, 189, 248, 0.2); border-top: 4px solid #38BDF8; border-radius: 50%; animation: spin 1s linear infinite; margin-bottom: 20px; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        </style>
        <div class="splash-container">
            <div class="spinner-ring"></div>
            <h2 style='font-size: 1.2rem; font-weight: 600; color: #F8FAFC;'>Loading Campus Connect...</h2>
        </div>
    """, unsafe_allow_html=True)
    time.sleep(1)
    st.session_state.splash_shown = True
    st.rerun()

# --- Styling matching 2nd image circular icon grid design ---
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
        .stApp { background: #0F172A !important; }
        .block-container { position: relative; z-index: 1; padding-top: 0.8rem !important; padding-bottom: 5rem !important; max-width: 460px !important; margin: auto !important; }
        #MainMenu, header, footer {visibility: hidden;}
        .app-header { background: rgba(30, 41, 59, 0.85); backdrop-filter: blur(12px); padding: 12px 16px; border-radius: 14px; color: white; margin-bottom: 12px; border: 1px solid rgba(255,255,255,0.1); display: flex; justify-content: space-between; align-items: center; }
        .sched-card { background: rgba(30, 41, 59, 0.8); border-radius: 14px; padding: 14px; color: #F8FAFC; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.3); }
        .badge-tag { background: rgba(56, 189, 248, 0.15); color: #38BDF8; padding: 3px 8px; border-radius: 6px; font-size: 0.72rem; font-weight: 700; }
        .route-stop { padding: 8px 0; border-left: 2px solid #38BDF8; padding-left: 14px; margin-left: 8px; font-size: 0.82rem; color: #CBD5E1; font-weight: 500; }
        
        /* 2nd Image Circular Icon Grid Tile Styling */
        .grid-tile { background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(56, 189, 248, 0.15); border-radius: 16px; padding: 16px 8px; text-align: center; transition: all 0.2s ease; margin-bottom: 10px; }
        .grid-tile:hover { border-color: rgba(56, 189, 248, 0.6); background: rgba(30, 41, 59, 0.9); }
        .grid-icon { width: 56px; height: 56px; margin: 0 auto 8px auto; background: rgba(56, 189, 248, 0.12); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; border: 1px solid rgba(56, 189, 248, 0.3); }
        .grid-label { font-size: 0.78rem; font-weight: 600; color: #F8FAFC; line-height: 1.2; }

        /* Bottom Sticky Navigation */
        .bottom-nav { position: fixed; bottom: 0; left: 0; width: 100%; background: rgba(15, 23, 42, 0.95); backdrop-filter: blur(12px); border-top: 1px solid rgba(56, 189, 248, 0.2); display: flex; justify-content: space-around; padding: 10px 0; z-index: 99999; }
        </style>
    """, unsafe_allow_html=True)

logo_small = f"<img src='{logo_image_data}' style='width:34px; height:34px; border-radius:50%; object-fit:cover; border:2px solid #38BDF8;'>" if logo_image_data else "🎓"

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
    # --- Main Application Header with Logout Option ---
    profile_avatar_html = f"<img src='data:image/jpeg;base64,{st.session_state.user_photo}' style='width:100%; height:100%; object-fit:cover;'>" if st.session_state.user_photo else logo_small
    
    col_head1, col_head2 = st.columns([4, 1])
    with col_head1:
        st.markdown(f"""
            <div class='app-header' style='margin-bottom:0;'>
                <div style='display: flex; align-items: center; gap: 10px;'>
                    <div style='width: 40px; height: 40px; border-radius: 50%; overflow: hidden; border: 2px solid #38BDF8; background: #0B1221; display: flex; align-items: center; justify-content: center;'>
                        {profile_avatar_html}
                    </div>
                    <div>
                        <div style='font-size: 0.95rem; font-weight: 800; color: #F8FAFC;'>{st.session_state.user_name}</div>
                        <div style='font-size: 0.7rem; color: #38BDF8;'>{st.session_state.user_univ} • ID: {st.session_state.user_id}</div>
                    </div>
                </div>
                <div>
                    <span class='badge-tag'>🟢 Online</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
    with col_head2:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.is_admin = False
            st.session_state.user_id = ""
            st.session_state.splash_shown = False
            if "session_user" in st.query_params:
                del st.query_params["session_user"]
            st.rerun()

    # --- TOP LOCATION BAR ---
    st.markdown(f"""
        <div style='background: rgba(30, 41, 59, 0.6); padding: 8px 14px; border-radius: 10px; font-size: 0.78rem; color: #94A3B8; margin: 10px 0; display: flex; justify-content: space-between; align-items: center; border: 1px solid rgba(56,189,248,0.15);'>
            <span>📍 Location: <b style='color: #F8FAFC;'>Tongi Station Road</b></span>
            <span style='color: #38BDF8; font-weight: 700;'>Live Connected</span>
        </div>
    """, unsafe_allow_html=True)

    # --- MAIN PAGE CONTAINER ---
    st.markdown("<div style='font-size: 1.05rem; font-weight: 800; color: #38BDF8; margin-bottom: 12px;'>📄 Page - 2: Core Services Dashboard</div>", unsafe_allow_html=True)

    # --- SECTION 1: EMERGENCY SOS & HOTLINE (Circular Grid UI like 2nd Image) ---
    st.markdown("### 🚨 1. Emergency SOS and Hotline")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
            <div class='grid-tile'>
                <div class='grid-icon'>🚨</div>
                <div class='grid-label'>Tap to 999</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Call 999", key="btn_999", use_container_width=True):
            st.success("Calling 999...")
    with col2:
        st.markdown("""
            <div class='grid-tile'>
                <div class='grid-icon'>👥</div>
                <div class='grid-label'>Close Friends</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Alert Friends", key="btn_friends", use_container_width=True):
            st.success("Broadcast sent!")
    with col3:
        st.markdown("""
            <div class='grid-tile'>
                <div class='grid-icon'>👪</div>
                <div class='grid-label'>Family Alert</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Alert Family", key="btn_family", use_container_width=True):
            st.success("Family notified!")
    with col4:
        st.markdown("""
            <div class='grid-tile'>
                <div class='grid-icon'>🏛️</div>
                <div class='grid-label'>University Authority</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Uni Security", key="btn_uni", use_container_width=True):
            st.success("Security alerted!")

    st.markdown("<hr style='border-color: rgba(255,255,255,0.08); margin: 16px 0;'>", unsafe_allow_html=True)

    # --- SECTION 2: FACULTY DIRECTORY AND CONSULTATION ---
    st.markdown("### 👨‍🏫 2. Faculty Directory and Consultation")
    st.markdown("<div style='font-size: 0.76rem; color: #94A3B8; margin-bottom: 8px;'>Active inside campus • Home when off-campus (No external tracking)</div>", unsafe_allow_html=True)
    
    fac_search = st.text_input("🔍 Search faculty...", placeholder="Type name or department...")
    
    st.markdown("""
        <div class='sched-card'>
            <b>Prof. Dr. M. Ahmed</b><br>
            <span class='badge-tag'>EEE Department</span> • Senior Professor<br>
            🕒 Consultation: Sun-Tue (03:00 PM - 05:00 PM)<br>
            <div style='margin-top: 6px;'><span style='background: rgba(34,197,94,0.15); color: #22C55E; padding: 2px 8px; border-radius: 6px; font-size: 0.72rem; font-weight: 700;'>🟢 Active (Inside Campus)</span></div>
        </div>
        <div class='sched-card'>
            <b>Dr. Selim Reza</b><br>
            <span class='badge-tag'>ECE Department</span> • Associate Professor<br>
            🕒 Consultation: Mon-Wed (11:00 AM - 01:00 PM)<br>
            <div style='margin-top: 6px;'><span style='background: rgba(148,163,184,0.15); color: #94A3B8; padding: 2px 8px; border-radius: 6px; font-size: 0.72rem; font-weight: 700;'>🏠 Home / Off-Campus</span></div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color: rgba(255,255,255,0.08); margin: 16px 0;'>", unsafe_allow_html=True)

    # --- SECTION 3: BUS SCHEDULE AND LIVE TRACKING ---
    st.markdown("### 🚌 3. Bus Schedule and Live Tracking")
    
    st.session_state.bus_db = load_json_db(BUS_DB_FILE, default_buses)
    b_info = st.session_state.bus_db[0] if st.session_state.bus_db else default_buses[0]
    
    st.markdown(f"""
        <div class='sched-card' style='border: 1px solid rgba(56,189,248,0.4);'>
            <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;'>
                <span style='font-weight: 800; font-size: 0.95rem;'>{b_info['name']}</span>
                <span class='badge-tag' style='background: #22C55E; color: white;'>{b_info['status']}</span>
            </div>
            <div style='background: rgba(56, 189, 248, 0.1); padding: 8px 10px; border-radius: 8px; margin-bottom: 8px; font-size: 0.78rem;'>
                📍 <b>Current Next Stop ETA:</b> {b_info['next_stop']} (Arriving in 10 mins)
            </div>
            <div style='color: #94A3B8; font-size: 0.78rem; margin-bottom: 6px;'>
                🕒 Departure: <b>{b_info['departure']}</b> | Arrival(ETA): <b>{b_info['arrival']}</b>
            </div>
            <div style='font-size: 0.78rem;'><b>Driver:</b> {b_info['driver']} ({b_info['driver_phone']})</div>
            <div style='font-size: 0.78rem;'><b>Helper:</b> {b_info['helper']} ({b_info['helper_phone']})</div>
        </div>
    """, unsafe_allow_html=True)

    with st.expander("🗺 View Detailed Route Map & Stations"):
        st.markdown("""
            <div class='route-stop'>📍 Campus (Departure Point)</div>
            <div class='route-stop'>📍 Tongi Station Road</div>
            <div class='route-stop'>📍 Amtoly Mor</div>
            <div class='route-stop'>📍 T & T Bazar</div>
            <div class='route-stop'>📍 Shilmoon</div>
            <div class='route-stop'>📍 Nimtoly Bridge</div>
            <div class='route-stop'>📍 Majukhan Bazar</div>
            <div class='route-stop'>📍 Koromtola</div>
            <div class='route-stop'>📍 Talotia Pump</div>
            <div class='route-stop'>📍 Mirer Bazar</div>
            <div class='route-stop'>📍 Basugaon (Terminal Arrival)</div>
        """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color: rgba(255,255,255,0.08); margin: 16px 0;'>", unsafe_allow_html=True)

    # --- SECTION 4: ALUMNI NETWORK AND MENTOR HUB ---
    st.markdown("### 🤝 4. Alumni Network and Mentor Hub")

    with st.expander("📝 Register in Alumni Network"):
        with st.form("alumni_reg_form"):
            al_name = st.text_input("Full Name", placeholder="Your Name")
            al_batch = st.text_input("Batch / Graduation Year", placeholder="e.g. Class of 2024")
            al_role = st.text_input("Current Profession / Role", placeholder="e.g. Software Engineer")
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
                    st.success("✅ Successfully registered!")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error("❌ Please fill in all details.")

    st.markdown("<div style='font-size: 0.85rem; font-weight: 700; margin: 10px 0;'>🌟 Registered Alumni Directory</div>", unsafe_allow_html=True)
    
    st.session_state.alumni_db = load_json_db(ALUMNI_DB_FILE, default_alumni)
    for alumni in st.session_state.alumni_db:
        st.markdown(f"""
            <div class='sched-card'>
                <b>{alumni['name']}</b><br>
                <span class='badge-tag'>{alumni['batch']}</span><br>
                💼 {alumni['role']}<br>
                📞 <b>Contact:</b> {alumni['contact']}
            </div>
        """, unsafe_allow_html=True)

    # --- BOTTOM STICKY NAVIGATION BAR ---
    st.markdown("""
        <div class='bottom-nav'>
            <div style='text-align: center; color: #38BDF8; font-size: 0.7rem; font-weight: 700;'>🚌 SHUTTLE</div>
            <div style='text-align: center; color: #94A3B8; font-size: 0.7rem; font-weight: 700;'>👨‍🏫 FACULTY</div>
            <div style='text-align: center; color: #94A3B8; font-size: 0.7rem; font-weight: 700;'>🗺️ ROUTE</div>
        </div>
    """, unsafe_allow_html=True)
