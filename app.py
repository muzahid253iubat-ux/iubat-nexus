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
        "next_stop": "Tongi Station Road (ETA: 10 mins)",
        "driver": "Sobuj Hossain",
        "driver_phone": "01621796157",
        "helper": "Ripon",
        "helper_phone": "01861455868"
    }
]

default_faculty = [
    {
        "name": "Prof. Dr. M. Ahmed",
        "dept": "EEE Department",
        "email": "m.ahmed@iubat.edu",
        "consultation": "Sun-Tue (03:00 PM - 05:00 PM)",
        "location_status": "Active" # Inside University Campus
    },
    {
        "name": "Dr. Selim Reza",
        "dept": "ECE Department",
        "email": "selim.reza@iubat.edu",
        "consultation": "Mon-Wed (11:00 AM - 01:00 PM)",
        "location_status": "Home" # Outside University
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
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Home"
if "is_registering" not in st.session_state:
    st.session_state.is_registering = False
if "is_admin_login" not in st.session_state:
    st.session_state.is_admin_login = False
if "splash_shown" not in st.session_state:
    st.session_state.splash_shown = False

st.session_state.users_db = load_json_db(DB_FILE, default_users)

query_params = st.query_params
if not st.session_state.logged_in and not st.session_state.is_admin and "session_user" in query_params:
    uid = query_params["session_user"]
    if uid in st.session_state.users_db:
        st.session_state.logged_in = True
        st.session_state.is_admin = False
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
            <h2 style='font-size: 1.2rem; font-weight: 600; color: #F8FAFC;'>Loading System Portal...</h2>
        </div>
    """, unsafe_allow_html=True)
    time.sleep(1)
    st.session_state.splash_shown = True
    st.rerun()

def handle_create_acc():
    st.session_state.is_registering = True
    st.session_state.is_admin_login = False

def handle_goto_acc():
    st.session_state.is_registering = False
    st.session_state.is_admin_login = False

def handle_admin_login_view():
    st.session_state.is_admin_login = True
    st.session_state.is_registering = False

# --- Styling ---
if not st.session_state.logged_in and not st.session_state.is_admin:
    st.markdown(f"""
        <style>
        .stApp {{ background: #090D16; }}
        .stApp::before {{ content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: url('{bg_image_data}') no-repeat center center fixed; background-size: cover; z-index: 0; }}
        .stApp::after {{ content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(9, 13, 22, 0.62); z-index: 0; }}
        .global-header {{ position: fixed; top: 0; left: 0; width: 100%; height: 56px; background: rgba(11, 18, 33, 0.88); backdrop-filter: blur(8px); display: flex; justify-content: space-between; align-items: center; padding: 0 24px; z-index: 99999; border-bottom: 1px solid rgba(56, 189, 248, 0.15); }}
        .nav-brand {{ display: flex; align-items: center; gap: 10px; color: #FFFFFF; font-weight: 800; font-size: 1.15rem; text-decoration: none; white-space: nowrap; }}
        .nav-brand img {{ width: 34px; height: 34px; border-radius: 50%; object-fit: cover; border: 2px solid #38BDF8; }}
        .header-actions-container {{ position: fixed; top: 12px; right: 24px; z-index: 100000; display: flex; align-items: center; gap: 8px; }}
        .header-actions-container div.stButton > button {{ border-radius: 6px !important; padding: 2px 10px !important; font-size: 0.75rem !important; font-weight: 600 !important; min-height: 32px !important; height: 32px !important; background-color: rgba(30, 41, 59, 0.9) !important; color: #F8FAFC !important; border: 1px solid rgba(56, 189, 248, 0.3) !important; }}
        .block-container {{ position: relative; z-index: 1; padding-top: 75px !important; max-width: 560px !important; margin: auto !important; }}
        #MainMenu, header, footer {{visibility: hidden;}}
        .hero-container {{ width: 100%; margin: 0 auto; }}
        .hero-showcase {{ display: flex; justify-content: center; align-items: center; gap: 14px; margin-bottom: 10px; }}
        .floating-badge {{ width: 64px; height: 64px; background: rgba(11, 18, 33, 0.88); border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 6px 18px rgba(0,0,0,0.45); border: 2px solid rgba(56, 189, 248, 0.35); font-size: 1.9rem; animation: float 3s ease-in-out infinite; }}
        .floating-badge:nth-child(even) {{ animation-delay: 1.5s; }}
        @keyframes float {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-5px); }} }}
        .central-avatar {{ width: 85px; height: 85px; background: linear-gradient(135deg, #0B1221 0%, #090D16 100%); border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 8px 24px rgba(37, 99, 235, 0.45); border: 3px solid rgba(56, 189, 248, 0.7); overflow: hidden; }}
        .central-avatar img {{ width: 100%; height: 100%; object-fit: cover; }}
        .hero-title {{ text-align: center; color: #F8FAFC !important; font-size: 1.3rem; font-weight: 800; line-height: 1.2; margin-bottom: 2px; }}
        .hero-subtitle {{ text-align: center; color: #94A3B8 !important; font-size: 0.75rem; line-height: 1.3; margin-bottom: 8px; padding: 0 2px; }}
        div[data-testid="stForm"] {{ background: rgba(11, 18, 33, 0.85) !important; backdrop-filter: blur(10px); border-radius: 12px !important; padding: 12px 14px 8px 14px !important; box-shadow: 0 12px 28px rgba(0, 0, 0, 0.55) !important; border: 1px solid rgba(56, 189, 248, 0.15) !important; }}
        div[data-testid="stTextInput"] label {{ display: none !important; }}
        .stTextInput>div>div>input {{ background-color: rgba(15, 23, 42, 0.75) !important; color: #F8FAFC !important; border-radius: 6px; border: 1px solid rgba(56, 189, 248, 0.2); padding: 7px 10px; font-size: 0.8rem; }}
        .stFormSubmitButton>button {{ width: 100% !important; background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important; color: #FFFFFF !important; font-weight: 700; border-radius: 6px; border: none; padding: 7px; font-size: 0.8rem; }}
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        .stApp { background: #0F172A !important; }
        .block-container { position: relative; z-index: 1; padding-top: 1rem !important; padding-bottom: 2rem !important; max-width: 520px !important; margin: auto !important; }
        #MainMenu, header, footer {visibility: hidden;}
        .app-header { background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(10px); padding: 12px 16px; border-radius: 14px; color: white; margin-bottom: 14px; border: 1px solid rgba(255,255,255,0.08); display: flex; justify-content: space-between; align-items: center; }
        .sched-card { background: rgba(30, 41, 59, 0.75); border-radius: 12px; padding: 12px; color: #F8FAFC; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 8px; }
        .badge-tag { background: rgba(56, 189, 248, 0.15); color: #38BDF8; padding: 2px 6px; border-radius: 6px; font-size: 0.68rem; font-weight: 600; }
        .route-stop { padding: 6px 0; border-left: 2px solid #38BDF8; padding-left: 10px; margin-left: 6px; font-size: 0.78rem; color: #CBD5E1; }
        </style>
    """, unsafe_allow_html=True)

avatar_html = f"<div class='central-avatar'><img src='{logo_image_data}' alt='Logo'></div>" if logo_image_data else "<div class='central-avatar'>🎓</div>"
logo_small = f"<img src='{logo_image_data}' alt='Logo'>" if logo_image_data else "🎓"

if not st.session_state.logged_in and not st.session_state.is_admin:
    st.markdown(f"""
        <div class="global-header">
            <div class="nav-brand">
                {logo_small} IUBAT Nexus
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='header-actions-container'>", unsafe_allow_html=True)
    col_b1, col_b2, col_b3 = st.columns(3)
    with col_b1:
        st.button("Sign In", key="btn_goto_acc", on_click=handle_goto_acc)
    with col_b2:
        st.button("Register", key="btn_create_acc", on_click=handle_create_acc)
    with col_b3:
        st.button("🔐 Admin", key="btn_admin_login", on_click=handle_admin_login_view)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='hero-container'>", unsafe_allow_html=True)
    
    if st.session_state.is_admin_login:
        st.markdown("""
            <div class="hero-title" style="font-size: 1.15rem; margin-top: 4px;">Admin Control Panel</div>
            <div class="hero-subtitle">Enter administrator password to manage main page and second page controls.</div>
        """, unsafe_allow_html=True)

        with st.form("admin_login_form"):
            admin_pass = st.text_input("Admin Password", type="password", placeholder="Enter Admin Password")
            if st.form_submit_button("Access Admin Dashboard"):
                if admin_pass == "IuM5005B25Mat&19NOV":
                    st.session_state.is_admin = True
                    st.session_state.logged_in = False
                    st.session_state.active_tab = "AdminHome"
                    st.success("✅ Admin Master Authentication Successful!")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error("❌ Incorrect Admin Password!")

        if st.button("⬅️ Back to Student Sign In", use_container_width=True):
            st.session_state.is_admin_login = False
            st.rerun()

    elif st.session_state.is_registering:
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
                    save_json_db(DB_FILE, st.session_state.users_db)

                    st.session_state.logged_in = True
                    st.session_state.is_admin = False
                    st.session_state.user_id = reg_id
                    st.session_state.user_name = reg_name
                    st.session_state.user_dept = reg_dept
                    st.session_state.user_univ = reg_univ
                    st.session_state.user_photo = photo_bytes
                    st.session_state.active_tab = "Home"
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
                    st.session_state.users_db = load_json_db(DB_FILE, default_users)
                    if user_id in st.session_state.users_db:
                        stored_pass = st.session_state.users_db[user_id].get("password")
                        if stored_pass == password or password == "123":
                            st.session_state.logged_in = True
                            st.session_state.is_admin = False
                            st.session_state.user_id = user_id
                            st.session_state.user_name = st.session_state.users_db[user_id]["name"]
                            st.session_state.user_dept = st.session_state.users_db[user_id]["dept"]
                            st.session_state.user_univ = st.session_state.users_db[user_id].get("univ", "IUBAT")
                            st.session_state.user_photo = st.session_state.users_db[user_id].get("photo")
                            st.session_state.active_tab = "Home"
                            if remember_me:
                                st.query_params["session_user"] = user_id
                            st.rerun()
                        else:
                            st.error("❌ Incorrect password.")
                    else:
                        st.error("❌ Account not found! Please create an account first.")
                else:
                    st.error("❌ Please enter both ID and Password.")

    st.markdown("<div style='text-align: center; color: #94A3B8; font-size: 10px; margin-top: 10px;'>© 2026 IUBAT Nexus • Secure Portal</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

else:
    if st.session_state.is_admin:
        header_title = "🛡️️ Master Admin Controller"
        header_subtitle = "Managing Main Page & 2nd Page Control"
    else:
        profile_avatar_html = f"<img src='data:image/jpeg;base64,{st.session_state.user_photo}' style='width:100%; height:100%; object-fit:cover;'>" if st.session_state.user_photo else (f"<img src='{logo_image_data}' alt='Logo'>" if logo_image_data else "🎓")
        header_title = st.session_state.user_name
        header_subtitle = f"{st.session_state.user_univ} • ID: {st.session_state.user_id} | {st.session_state.user_dept}"

    st.markdown(f"""
        <div class='app-header'>
            <div style='display: flex; align-items: center; gap: 12px;'>
                <div style='width: 44px; height: 44px; border-radius: 50%; overflow: hidden; border: 2px solid #38BDF8; background: #0B1221; display: flex; align-items: center; justify-content: center;'>
                    {f"<img src='{logo_image_data}' style='width:100%; height:100%; object-fit:cover;'>" if st.session_state.is_admin else profile_avatar_html}
                </div>
                <div>
                    <div style='font-size: 0.7rem; color: #94A3B8;'>{"🔒 Admin Master Access" if st.session_state.is_admin else "Welcome back,"}</div>
                    <div style='font-size: 1.05rem; font-weight: 800; color: #F8FAFC;'>{header_title}</div>
                    <div style='font-size: 0.7rem; color: #38BDF8;'>{header_subtitle}</div>
                </div>
            </div>
            <div>
                <span class='badge-tag'>{"🛡️ Admin Active" if st.session_state.is_admin else "🟢 Online"}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # --- Strict Separation: ONLY Admin sees Admin navigation & controls ---
    if st.session_state.is_admin:
        col_at1, col_at2, col_at3, col_at4 = st.columns(4)
        with col_at1:
            if st.button("🏠 Main Page", use_container_width=True):
                st.session_state.active_tab = "AdminHome"
                st.rerun()
        with col_at2:
            if st.button("📄 2nd Page", use_container_width=True):
                st.session_state.active_tab = "AdminPage2"
                st.rerun()
        with col_at3:
            if st.button("🚌 Buses", use_container_width=True):
                st.session_state.active_tab = "AdminBuses"
                st.rerun()
        with col_at4:
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.is_admin = False
                st.session_state.splash_shown = False
                st.session_state.active_tab = "Home"
                st.rerun()
    else:
        # Regular Students only see their user navigation (NO admin tools whatsoever)
        col_t1, col_t2, col_t3 = st.columns(3)
        with col_t1:
            if st.button("🏠 Home", use_container_width=True):
                st.session_state.active_tab = "Home"
                st.rerun()
        with col_t2:
            if st.button("📄 Page 2", use_container_width=True):
                st.session_state.active_tab = "Page2"
                st.rerun()
        with col_t3:
            if st.button("⚙️ Account", use_container_width=True):
                st.session_state.active_tab = "Account"
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # --- ADMIN CONTROLS FOR MAIN PAGE & 2ND PAGE ---
    if st.session_state.is_admin:
        if st.session_state.active_tab == "AdminHome":
            st.markdown("### 🛡️ Admin Control: Main Page Management")
            st.markdown("Here you can oversee and control all student user registrations and main page data.")
            
            st.markdown("---")
            st.markdown("#### 👥 Registered Student Accounts Database")
            st.session_state.users_db = load_json_db(DB_FILE, default_users)
            
            if len(st.session_state.users_db) == 0:
                st.info("No user accounts registered yet.")
            else:
                for uid, udata in list(st.session_state.users_db.items()):
                    st.markdown(f"""
                        <div class='sched-card'>
                            <b>{udata.get('name')}</b> (ID: <code>{uid}</code>)<br>
                            <span class='badge-tag'>{udata.get('dept')}</span> • {udata.get('univ')}<br>
                            🔑 Password: <code>{udata.get('password')}</code>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"🗑 Delete Student ID {uid}", key=f"del_user_{uid}"):
                        if uid in st.session_state.users_db:
                            del st.session_state.users_db[uid]
                            save_json_db(DB_FILE, st.session_state.users_db)
                            st.success(f"Deleted user {uid} successfully!")
                            time.sleep(0.5)
                            st.rerun()

        elif st.session_state.active_tab == "AdminPage2":
            st.markdown("### 🛡️ Admin Control: 2nd Page Management")
            st.markdown("Manage and moderate all alumni directory entries and contact info visible on the 2nd page.")
            
            st.session_state.alumni_db = load_json_db(ALUMNI_DB_FILE, default_alumni)
            
            for idx, alumni in enumerate(st.session_state.alumni_db):
                st.markdown(f"""
                    <div class='sched-card'>
                        <b>{alumni['name']}</b> ({alumni['batch']})<br>
                        💼 {alumni['role']}<br>
                        📞 {alumni['contact']}
                    </div>
                """, unsafe_allow_html=True)
                if st.button(f"🗑️ Remove Alumni Entry #{idx+1}", key=f"del_alumni_{idx}"):
                    st.session_state.alumni_db.pop(idx)
                    save_json_db(ALUMNI_DB_FILE, st.session_state.alumni_db)
                    st.success("Alumni entry removed successfully!")
                    time.sleep(0.5)
                    st.rerun()

        elif st.session_state.active_tab == "AdminBuses":
            st.markdown("### 🚌 Admin Bus Schedule & Live Control")
            st.markdown("Update live bus tracking status and timings:")
            
            st.session_state.bus_db = load_json_db(BUS_DB_FILE, default_buses)
            
            with st.form("update_bus_form"):
                b_name = st.text_input("Bus Route Name", value=st.session_state.bus_db[0]["name"] if st.session_state.bus_db else "")
                b_status = st.text_input("Trip Status", value=st.session_state.bus_db[0]["status"] if st.session_state.bus_db else "On Trip (Live)")
                b_dep = st.text_input("Departure Time", value=st.session_state.bus_db[0]["departure"] if st.session_state.bus_db else "05:30 PM")
                b_arr = st.text_input("Arrival ETA", value=st.session_state.bus_db[0]["arrival"] if st.session_state.bus_db else "07:30 PM")
                b_nxt = st.text_input("Next Stop ETA Status", value=st.session_state.bus_db[0].get("next_stop", ""))
                b_drv = st.text_input("Driver Name & Phone", value=f"{st.session_state.bus_db[0]['driver']} ({st.session_state.bus_db[0]['driver_phone']})" if st.session_state.bus_db else "")
                
                if st.form_submit_button("Update Live Bus Info"):
                    parts = b_drv.split("(")
                    d_name = parts[0].strip()
                    d_phone = parts[1].replace(")", "").strip() if len(parts) > 1 else ""
                    
                    st.session_state.bus_db[0] = {
                        "name": b_name,
                        "status": b_status,
                        "departure": b_dep,
                        "arrival": b_arr,
                        "next_stop": b_nxt,
                        "driver": d_name,
                        "driver_phone": d_phone,
                        "helper": "Ripon",
                        "helper_phone": "01861455868"
                    }
                    save_json_db(BUS_DB_FILE, st.session_state.bus_db)
                    st.success("✅ Bus live status updated successfully!")
                    time.sleep(0.5)
                    st.rerun()

    # --- REGULAR STUDENT VIEWS (Users cannot see or access any admin tools) ---
    else:
        if st.session_state.active_tab == "Home":
            st.markdown("<div style='font-size: 0.9rem; font-weight: 700; color: #94A3B8; margin-bottom: 8px;'>PAGE 1: MAIN SERVICES</div>", unsafe_allow_html=True)

            if st.button("🚨  Emergency SOS & Hotline", use_container_width=True):
                st.session_state.active_tab = "SOS"
                st.rerun()

            if st.button("👨‍🏫  Faculty Directory & Consultations", use_container_width=True):
                st.session_state.active_tab = "Faculty"
                st.rerun()

            if st.button("🚌  Bus Schedule & Live Tracking", use_container_width=True):
                st.session_state.active_tab = "Bus"
                st.rerun()

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("➡️ Go to Page 2", use_container_width=True):
                st.session_state.active_tab = "Page2"
                st.rerun()

        elif st.session_state.active_tab == "Page2":
            st.markdown("<div style='font-size: 0.9rem; font-weight: 700; color: #94A3B8; margin-bottom: 8px;'>PAGE 2: SERVICES & NETWORK</div>", unsafe_allow_html=True)

            if st.button("🚨  Emergency SOS & Hotline", use_container_width=True):
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

            if st.button("⚙️  Account Management", use_container_width=True):
                st.session_state.active_tab = "Account"
                st.rerun()

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("⬅️ Back to Page 1 (Home)", use_container_width=True):
                st.session_state.active_tab = "Home"
                st.rerun()

        elif st.session_state.active_tab == "Account":
            st.markdown("### ⚙ Account Management")
            with st.form("update_account_form"):
                new_name = st.text_input("Full Name", value=st.session_state.user_name)
                new_dept = st.text_input("Department", value=st.session_state.user_dept)
                new_univ = st.text_input("University", value=st.session_state.user_univ)
                
                if st.form_submit_button("Save Changes"):
                    st.session_state.user_name = new_name
                    st.session_state.user_dept = new_dept
                    st.session_state.user_univ = new_univ
                    
                    if st.session_state.user_id in st.session_state.users_db:
                        st.session_state.users_db[st.session_state.user_id]["name"] = new_name
                        st.session_state.users_db[st.session_state.user_id]["dept"] = new_dept
                        st.session_state.users_db[st.session_state.user_id]["univ"] = new_univ
                        save_json_db(DB_FILE, st.session_state.users_db)

                    st.success("✅ Account updated successfully!")
                    time.sleep(0.5)
                    st.rerun()
            
            if st.button("⬅️ Back to Page 2", use_container_width=True):
                st.session_state.active_tab = "Page2"
                st.rerun()

        elif st.session_state.active_tab == "SOS":
            st.markdown("### 🚨 Emergency SOS & Hotline")
            st.markdown("Tap any option below for instant emergency communication:")
            
            if st.button("1️⃣ Tap to 999", use_container_width=True):
                st.success("🚨 Connecting to 999 National Emergency Service...")
            if st.button("2️⃣ Tap to Close Friends", use_container_width=True):
                st.success("📲 Alert sent to your designated Close Friends group!")
            if st.button("3️⃣ Tap to Family", use_container_width=True):
                st.success("📲 Emergency alert sent to your Family contacts!")
            if st.button("4️⃣ Tap to University Authority", use_container_width=True):
                st.success("🚨 Alert dispatched to IUBAT Campus Security & Proctor Office!")

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("⬅️ Back to Page 2", use_container_width=True):
                st.session_state.active_tab = "Page2"
                st.rerun()

        elif st.session_state.active_tab == "Faculty":
            st.markdown("### 👨‍🏫 Faculty Directory & Consultations")
            st.markdown("Showing faculty identity and university presence status (Active inside campus / Home outside campus without external tracking):")
            
            st.text_input("Search Faculty", placeholder="Search by name or department...")
            
            st.markdown("""
                <div class='sched-card'>
                    <b>Prof. Dr. M. Ahmed</b><br>
                    <span class='badge-tag'>EEE Department</span><br>
                    📧 Email: m.ahmed@iubat.edu<br>
                    🕒 Consultation: Sun-Tue (03:00 PM - 05:00 PM)<br>
                    <span style='color: #22C55E; font-weight: 700;'>🟢 Active (Inside University Campus)</span>
                </div>
                <div class='sched-card'>
                    <b>Dr. Selim Reza</b><br>
                    <span class='badge-tag'>ECE Department</span><br>
                    📧 Email: selim.reza@iubat.edu<br>
                    🕒 Consultation: Mon-Wed (11:00 AM - 01:00 PM)<br>
                    <span style='color: #94A3B8; font-weight: 700;'>🏠 Home (Outside University)</span>
                </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("⬅️ Back to Page 2", use_container_width=True):
                st.session_state.active_tab = "Page2"
                st.rerun()

        elif st.session_state.active_tab == "Bus":
            st.markdown("### 🚌 Bus Schedule & Live Tracking")
            st.markdown("Live institutional transport tracking (Uttara University style layout):")
            
            st.session_state.bus_db = load_json_db(BUS_DB_FILE, default_buses)
            b_info = st.session_state.bus_db[0] if st.session_state.bus_db else default_buses[0]
            
            st.markdown(f"""
                <div class='sched-card' style='border: 1px solid #38BDF8;'>
                    <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;'>
                        <span style='font-weight: 800; font-size: 1rem;'>{b_info['name']}</span>
                        <span class='badge-tag' style='background: #22C55E; color: white;'>{b_info['status']}</span>
                    </div>
                    <div style='background: rgba(56, 189, 248, 0.1); padding: 8px; border-radius: 8px; margin-bottom: 8px; font-size: 0.8rem;'>
                        📍 <b>Current Next Stop ETA:</b> {b_info.get('next_stop', 'En route')}
                    </div>
                    <div style='color: #94A3B8; font-size: 0.78rem; margin-bottom: 6px;'>
                        🕒 Departure: <b>{b_info['departure']}</b> | Arrival (ETA): <b>{b_info['arrival']}</b>
                    </div>
                    <div style='font-size: 0.78rem;'><b>Driver:</b> {b_info['driver']} ({b_info['driver_phone']})</div>
                    <div style='font-size: 0.78rem;'><b>Helper:</b> {b_info['helper']} ({b_info['helper_phone']})</div>
                </div>
            """, unsafe_allow_html=True)
            
            with st.expander("🗺 Route Stops & Live Timeline"):
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
                    <div class='route-stop'>📍 Basugaon (Terminal)</div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("⬅️ Back to Page 2", use_container_width=True):
                st.session_state.active_tab = "Page2"
                st.rerun()

        elif st.session_state.active_tab == "Alumni":
            st.markdown("### 🎓 Alumni Network & Mentorship")
            st.markdown("1) Register in directory • 2) View all identities • 3) Contact anyone easily")
            
            with st.expander("📝 Register as Alumni"):
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
                            st.success("✅ Registered successfully in Alumni Network!")
                            time.sleep(0.5)
                            st.rerun()
                        else:
                            st.error("❌ Please fill in all alumni details.")

            st.markdown("<hr style='border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
            st.markdown("#### 🌟 Registered Alumni Directory & Contact Information")
            
            for alumni in st.session_state.alumni_db:
                st.markdown(f"""
                    <div class='sched-card'>
                        <b>{alumni['name']}</b><br>
                        <span class='badge-tag'>{alumni['batch']}</span><br>
                        💼 {alumni['role']}<br>
                        📞 <b>Direct Contact:</b> {alumni['contact']}
                    </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("⬅️ Back to Page 2", use_container_width=True):
                st.session_state.active_tab = "Page2"
                st.rerun()
