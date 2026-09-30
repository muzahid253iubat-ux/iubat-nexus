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
            "name": "Abdullah Al Muzahid",
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
        .stApp { background: #070B14; }
        .splash-container {
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            height: 85vh; color: white; font-family: sans-serif;
        }
        .spinner-ring {
            width: 55px; height: 55px; border: 4px solid rgba(14, 165, 233, 0.2);
            border-top: 4px solid #0EA5E9; border-radius: 50%;
            animation: spin 0.9s linear infinite; margin-bottom: 20px;
        }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        </style>
        <div class="splash-container">
            <div class="spinner-ring"></div>
            <h2 style='font-size: 1.25rem; font-weight: 600; color: #F1F5F9; letter-spacing: 0.5px;'>Loading IUBAT Nexus Portal...</h2>
        </div>
    """, unsafe_allow_html=True)
    time.sleep(0.8)
    st.session_state.splash_shown = True
    st.rerun()

def handle_create_acc():
    st.session_state.is_registering = True

def handle_goto_acc():
    st.session_state.is_registering = False

# --- Global Styling ---
if not st.session_state.logged_in:
    st.markdown(f"""
        <style>
        .stApp {{ background: #070B14; }}
        .stApp::before {{
            content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: url('{bg_image_data}') no-repeat center center fixed; background-size: cover; z-index: 0;
        }}
        .stApp::after {{
            content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(7, 11, 20, 0.82); z-index: 0;
        }}
        .global-header {{
            position: fixed; top: 0; left: 0; width: 100%; height: 65px;
            background: rgba(11, 17, 32, 0.9); backdrop-filter: blur(12px);
            display: flex; justify-content: space-between; align-items: center;
            padding: 0 35px; z-index: 99999; border-bottom: 1px solid rgba(56, 189, 248, 0.15);
        }}
        .nav-brand {{
            display: flex; align-items: center; gap: 12px; color: #FFFFFF; font-weight: 800; font-size: 1.3rem; text-decoration: none;
        }}
        .nav-brand img {{ width: 38px; height: 38px; border-radius: 50%; object-fit: cover; border: 2px solid #0EA5E9; }}
        .header-actions-container {{
            position: fixed; top: 14px; right: 35px; z-index: 100000;
            display: flex; align-items: center; gap: 12px;
        }}
        .header-actions-container div.stButton > button {{
            border-radius: 8px !important; padding: 6px 18px !important; font-size: 0.82rem !important;
            font-weight: 600 !important; background-color: rgba(30, 41, 59, 0.95) !important; color: #F1F5F9 !important;
            border: 1px solid rgba(14, 165, 233, 0.35) !important; transition: all 0.3s ease;
        }}
        .block-container {{
            position: relative; z-index: 1; padding-top: 90px !important; max-width: 650px !important; margin: auto !important;
        }}
        #MainMenu, header, footer {{visibility: hidden;}}
        .hero-container {{ width: 100%; margin: 0 auto; padding: 10px 20px; }}
        .hero-showcase {{ display: flex; justify-content: center; align-items: center; gap: 16px; margin-bottom: 15px; }}
        .floating-badge {{
            width: 58px; height: 58px; background: rgba(15, 23, 42, 0.9); border-radius: 50%;
            display: flex; align-items: center; justify-content: center; box-shadow: 0 8px 20px rgba(0,0,0,0.5);
            border: 2px solid rgba(14, 165, 233, 0.3); font-size: 1.7rem; animation: float 3s ease-in-out infinite;
        }}
        @keyframes float {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-6px); }} }}
        .central-avatar {{
            width: 90px; height: 90px; background: linear-gradient(135deg, #0B1120 0%, #070B14 100%);
            border-radius: 50%; display: flex; align-items: center; justify-content: center;
            box-shadow: 0 10px 30px rgba(14, 165, 233, 0.4); border: 3px solid rgba(14, 165, 233, 0.8); overflow: hidden;
        }}
        .central-avatar img {{ width: 100%; height: 100%; object-fit: cover; }}
        .hero-title {{ text-align: center; color: #FFFFFF !important; font-size: 1.8rem; font-weight: 800; margin-bottom: 6px; letter-spacing: -0.5px; }}
        .hero-subtitle {{ text-align: center; color: #94A3B8 !important; font-size: 0.9rem; margin-bottom: 22px; line-height: 1.4; }}
        div[data-testid="stForm"] {{
            background: rgba(15, 23, 42, 0.88) !important; backdrop-filter: blur(16px);
            border-radius: 16px !important; padding: 24px 28px !important;
            border: 1px solid rgba(14, 165, 233, 0.2) !important; box-shadow: 0 15px 35px rgba(0,0,0,0.5);
        }}
        .stTextInput>div>div>input {{
            background-color: rgba(30, 41, 59, 0.7) !important; color: #F1F5F9 !important; border-radius: 8px;
            border: 1px solid rgba(14, 165, 233, 0.25); padding: 10px 14px; font-size: 0.92rem;
        }}
        .stFormSubmitButton>button {{
            width: 100% !important; background: linear-gradient(135deg, #0284C7 0%, #0369A1 100%) !important;
            color: #FFFFFF !important; font-weight: 700; border-radius: 8px; border: none; padding: 11px; font-size: 1rem;
            box-shadow: 0 4px 15px rgba(2, 132, 199, 0.4);
        }}
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        .stApp { background: #080C15 !important; color: #F1F5F9 !important; }
        .block-container { position: relative; z-index: 1; padding-top: 1.2rem !important; padding-bottom: 110px !important; max-width: 720px !important; margin: auto !important; }
        #MainMenu, header, footer {visibility: hidden;}

        .top-dash-header {
            background: rgba(15, 23, 42, 0.85); backdrop-filter: blur(16px); border: 1px solid rgba(14, 165, 233, 0.2);
            border-radius: 18px; padding: 14px 20px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 18px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        }
        .user-profile-pill {
            display: flex; align-items: center; gap: 12px;
        }
        .user-avatar-frame {
            width: 44px; height: 44px; border-radius: 50%; overflow: hidden; border: 2px solid #0EA5E9; background: #1E293B;
            display: flex; align-items: center; justify-content: center; font-size: 1.2rem;
        }
        .user-avatar-frame img { width: 100%; height: 100%; object-fit: cover; }
        .location-badge-pro {
            background: rgba(30, 41, 59, 0.9); border: 1px solid rgba(14, 165, 233, 0.3); padding: 6px 14px; border-radius: 30px; font-size: 0.85rem; color: #E2E8F0; display: flex; align-items: center; gap: 8px; font-weight: 500;
        }
        .sched-main-card-pro {
            background: rgba(15, 23, 42, 0.9); backdrop-filter: blur(16px); border-radius: 20px; padding: 22px; color: #F1F5F9;
            border: 1px solid rgba(14, 165, 233, 0.25); margin-bottom: 18px; box-shadow: 0 12px 35px rgba(0,0,0,0.4);
        }
        .badge-tag-pro {
            background: rgba(14, 165, 233, 0.15); color: #38BDF8; padding: 4px 10px; border-radius: 8px; font-size: 0.75rem; font-weight: 700; letter-spacing: 0.3px;
        }
        .route-stop-pro {
            padding: 8px 0; border-left: 3px solid #0EA5E9; padding-left: 14px; margin-left: 8px; font-size: 0.88rem; color: #CBD5E1; font-weight: 500;
        }

        /* --- Unique Floating Bottom Navigation Dock (Horizontal 1 Line) --- */
        .bottom-nav-dock {
            position: fixed; bottom: 16px; left: 50%; transform: translateX(-50%); width: 94%; max-width: 650px;
            background: rgba(15, 23, 42, 0.94); backdrop-filter: blur(20px);
            border: 1px solid rgba(14, 165, 233, 0.35); border-radius: 24px;
            display: flex; justify-content: space-around; align-items: center; padding: 8px 12px; z-index: 99999;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.6);
        }
        .bottom-nav-dock div.stButton > button {
            background: transparent !important; border: none !important; color: #94A3B8 !important;
            font-size: 0.85rem !important; font-weight: 600 !important; box-shadow: none !important;
            display: flex !important; flex-direction: row !important; align-items: center !important; justify-content: center !important;
            gap: 6px !important; padding: 6px 12px !important; min-height: 40px !important; border-radius: 12px !important;
            transition: all 0.2s ease-in-out; white-space: nowrap !important;
        }
        .bottom-nav-dock div.stButton > button:hover {
            color: #38BDF8 !important; background: rgba(14, 165, 233, 0.12) !important; transform: translateY(-2px);
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
        st.button("Create Account", key="btn_create_acc", on_click=handle_create_acc)
    with col_b2:
        st.button("Sign In", key="btn_goto_acc", on_click=handle_goto_acc)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='hero-container'>", unsafe_allow_html=True)
    
    if st.session_state.is_registering:
        st.markdown("""
            <div class="hero-title">Create IUBAT Account</div>
            <div class="hero-subtitle">Enter your details below to register your student portal profile.</div>
        """, unsafe_allow_html=True)

        with st.form("register_form"):
            reg_name = st.text_input("Full Name", placeholder="Full Name")
            reg_id = st.text_input("ID Number", placeholder="Student ID Number")
            reg_dept = st.text_input("Department", placeholder="Department (e.g. EEE)")
            reg_univ = st.text_input("University", placeholder="University Name", value="IUBAT")
            reg_pass = st.text_input("Password", type="password", placeholder="Create Password")
            reg_photo = st.file_uploader("Upload Profile Photo (Optional)", type=["jpg", "png", "jpeg"])

            if st.form_submit_button("Complete Registration & Enter Portal"):
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
            <div class="hero-showcase">
                <div class="floating-badge">🚨</div>
                <div class="floating-badge">👨‍🏫</div>
                {avatar_html}
                <div class="floating-badge">🚌</div>
                <div class="floating-badge">🎓</div>
            </div>
            <div class="hero-title">All of IUBAT,<br>Working For You</div>
            <div class="hero-subtitle">Sign in with your student ID and password to access smart shuttle schedules, faculty directories, and campus updates.</div>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            user_id = st.text_input("ID Number", placeholder="Student ID Number")
            password = st.text_input("Password", type="password", placeholder="Password")

            col1, col2 = st.columns([1.2, 1])
            with col1:
                remember_me = st.checkbox("Remember session")
            with col2:
                st.markdown("<div style='text-align: right; padding-top: 4px;'><a href='#' style='color: #38BDF8; font-size: 0.8rem; text-decoration: none;'>Forgot Password?</a></div>", unsafe_allow_html=True)

            if st.form_submit_button("Sign In to Portal"):
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
                            st.error("❌ Incorrect password. Try '123'.")
                    else:
                        st.error("❌ Account not found! Please create an account first.")
                else:
                    st.error("❌ Please enter both Student ID and Password.")

    st.markdown("<div style='text-align: center; color: #64748B; font-size: 12px; margin-top: 20px;'>© 2026 IUBAT Nexus • Smart University Portal</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # --- PRO FULL-WIDTH DASHBOARD ---
    photo_render = f"<img src='data:image/jpeg;base64,{st.session_state.user_photo}'>" if st.session_state.user_photo else "🎓"
    
    st.markdown(f"""
        <div class='top-dash-header'>
            <div class='user-profile-pill'>
                <div class='user-avatar-frame'>
                    {photo_render}
                </div>
                <div>
                    <div style='font-size: 0.95rem; font-weight: 800; color: #F1F5F9;'>{st.session_state.user_name}</div>
                    <div style='font-size: 0.72rem; color: #38BDF8;'>{st.session_state.user_dept}</div>
                </div>
            </div>
            <div class='location-badge-pro'>
                📍 Tongi Station Road
            </div>
            <div style='font-size: 1.3rem; cursor: pointer;'>🔔</div>
        </div>
    """, unsafe_allow_html=True)

    search_q = st.text_input("Search buses, routes, or faculty...", placeholder="🔍 Search campus transport or faculty...", label_visibility="collapsed")

    if st.session_state.dashboard_view == "Shuttle":
        st.markdown("<div style='font-size: 1.25rem; font-weight: 800; margin: 16px 0 6px 0; color: #F1F5F9;'>Shuttle Bus Schedule</div>", unsafe_allow_html=True)
        st.markdown("<div style='font-size: 0.85rem; color: #94A3B8; margin-bottom: 14px;'>📅 Today Schedule • <span style='color: #38BDF8; cursor: pointer;'>View full timetable</span></div>", unsafe_allow_html=True)

        st.markdown("""
            <div class='sched-main-card-pro'>
                <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;'>
                    <div style='display: flex; align-items: center; gap: 8px;'>
                        <span style='font-size: 1.4rem;'>🚌</span>
                        <span style='font-weight: 800; font-size: 1.15rem;'>Bus 02</span>
                        <span class='badge-tag-pro' style='background: rgba(239, 68, 68, 0.2); color: #F87171;'>Down Time</span>
                    </div>
                    <span style='font-size: 1.4rem;'>🗺️</span>
                </div>
                <div style='font-size: 0.92rem; color: #94A3B8; margin-bottom: 16px; font-weight: 500;'>
                    🚏 Route: Campus to Narshingdi
                </div>
                <div style='display: flex; justify-content: space-between; align-items: center; background: rgba(30, 41, 59, 0.6); padding: 14px 18px; border-radius: 12px; margin-bottom: 16px;'>
                    <div>
                        <div style='font-size: 1.15rem; font-weight: 800; color: #F1F5F9;'>05:30 PM</div>
                        <div style='font-size: 0.78rem; color: #94A3B8;'>Departure • Campus</div>
                    </div>
                    <div style='color: #0EA5E9; font-weight: 800; font-size: 1.2rem;'>➔</div>
                    <div style='text-align: right;'>
                        <div style='font-size: 1.15rem; font-weight: 800; color: #F1F5F9;'>07:30 PM</div>
                        <div style='font-size: 0.78rem; color: #94A3B8;'>Arrival (ETA) • Velanagor</div>
                    </div>
                </div>
                <div style='font-size: 0.88rem; margin-bottom: 10px; color: #CBD5E1;'>
                    <b>RouteMap:</b> Campus » Tongi Station Road » Amtoly Mor » T & T Bazar » Shilmoon
                </div>
                <hr style='border-color: rgba(255,255,255,0.08); margin: 14px 0;'>
                <div style='display: flex; justify-content: space-between; align-items: center; font-size: 0.9rem;'>
                    <div><b>Driver:</b> Sobuj Hossain <br><span style='color: #94A3B8; font-size: 0.8rem;'>📞 01621796157</span></div>
                    <span style='background: rgba(14, 165, 233, 0.2); padding: 8px 14px; border-radius: 10px; color: #38BDF8; font-weight: 600;'>Call Driver</span>
                </div>
                <div style='display: flex; justify-content: space-between; align-items: center; font-size: 0.9rem; margin-top: 12px;'>
                    <div><b>Helper:</b> Ripon <br><span style='color: #94A3B8; font-size: 0.8rem;'>📞 01861455868</span></div>
                    <span style='background: rgba(14, 165, 233, 0.2); padding: 8px 14px; border-radius: 10px; color: #38BDF8; font-weight: 600;'>Call Helper</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        if st.button("🗺️ Launch Live GPS Tracking", use_container_width=True, type="primary"):
            st.success("🟢 Bus 02 is currently active near Tongi Station Road. Speed: 32 km/h.")

    elif st.session_state.dashboard_view == "Faculty":
        st.markdown("<div style='font-size: 1.25rem; font-weight: 800; margin: 16px 0;'>Faculty Directory & Office Hours</div>", unsafe_allow_html=True)
        st.markdown("""
            <div class='sched-main-card-pro'>
                <div style='font-size: 1.1rem; font-weight: 800; color: #F1F5F9;'>Prof. Dr. M. Ahmed</div>
                <span class='badge-tag-pro'>EEE Department</span><br><br>
                <div style='font-size: 0.9rem; color: #CBD5E1;'>📧 m.ahmed@iubat.edu<br>🕒 Office Hours: Sun-Tue (03:00 PM - 05:00 PM)</div>
            </div>
            <div class='sched-main-card-pro'>
                <div style='font-size: 1.1rem; font-weight: 800; color: #F1F5F9;'>Dr. Selim Reza</div>
                <span class='badge-tag-pro'>ECE Department</span><br><br>
                <div style='font-size: 0.9rem; color: #CBD5E1;'>📧 selim.reza@iubat.edu<br>🕒 Office Hours: Mon-Wed (11:00 AM - 01:00 PM)</div>
            </div>
        """, unsafe_allow_html=True)

    elif st.session_state.dashboard_view == "Route":
        st.markdown("<div style='font-size: 1.25rem; font-weight: 800; margin: 16px 0;'>Route Stoppages (Campus to Narshingdi)</div>", unsafe_allow_html=True)
        st.markdown("""
            <div class='sched-main-card-pro'>
                <div class='route-stop-pro'>📍 Campus (Uttara) - Starting Point</div>
                <div class='route-stop-pro'>📍 Tongi Station Road</div>
                <div class='route-stop-pro'>📍 Amtoly Mor</div>
                <div class='route-stop-pro'>📍 T & T Bazar</div>
                <div class='route-stop-pro'>📍 Shilmoon</div>
                <div class='route-stop-pro'>📍 Nimtoly Bridge</div>
                <div class='route-stop-pro'>📍 Majukhan Bazar</div>
                <div class='route-stop-pro'>📍 Koromtola</div>
                <div class='route-stop-pro'>📍 Talotia Pump (Destination)</div>
            </div>
        """, unsafe_allow_html=True)

    elif st.session_state.dashboard_view == "SOS":
        st.markdown("<div style='font-size: 1.25rem; font-weight: 800; margin: 16px 0;'>Emergency SOS & Helplines</div>", unsafe_allow_html=True)
        st.markdown("""
            <div class='sched-main-card-pro' style='border-left: 5px solid #EF4444;'>
                <div style='font-size: 1.1rem; font-weight: 800; color: #F1F5F9;'>Campus Security Control Room</div>
                <div style='font-size: 0.9rem; color: #CBD5E1; margin-top: 6px;'>📞 Hotline: +880 1713-393291</div>
            </div>
            <div class='sched-main-card-pro' style='border-left: 5px solid #F59E0B;'>
                <div style='font-size: 1.1rem; font-weight: 800; color: #F1F5F9;'>Medical Center Emergency</div>
                <div style='font-size: 0.9rem; color: #CBD5E1; margin-top: 6px;'>📞 Ambulance: +880 1819-000000</div>
            </div>
        """, unsafe_allow_html=True)

    elif st.session_state.dashboard_view == "Account":
        st.markdown("<div style='font-size: 1.25rem; font-weight: 800; margin: 16px 0;'>Student Account & Settings</div>", unsafe_allow_html=True)
        with st.form("dash_acc_form"):
            up_name = st.text_input("Full Name", value=st.session_state.user_name)
            up_dept = st.text_input("Department", value=st.session_state.user_dept)
            if st.form_submit_button("Save Changes"):
                st.session_state.user_name = up_name
                st.session_state.user_dept = up_dept
                if st.session_state.user_id in st.session_state.users_db:
                    st.session_state.users_db[st.session_state.user_id]["name"] = up_name
                    st.session_state.users_db[st.session_state.user_id]["dept"] = up_dept
                    save_users_db(st.session_state.users_db)
                st.success("Profile updated successfully!")
                time.sleep(0.5)
                st.rerun()
        if st.button("🚪 Logout from Portal", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.splash_shown = False
            if "session_user" in st.query_params:
                del st.query_params["session_user"]
            st.rerun()

    # --- Floating Bottom Navigation Dock (1-line horizontal style) ---
    st.markdown("<div class='bottom-nav-dock'>", unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        if st.button("🚌 Shuttle", key="nav_shuttle"):
            st.session_state.dashboard_view = "Shuttle"
            st.rerun()
    with c2:
        if st.button("👨‍🏫 Faculty", key="nav_faculty"):
            st.session_state.dashboard_view = "Faculty"
            st.rerun()
    with c3:
        if st.button("🗺️ Route", key="nav_route"):
            st.session_state.dashboard_view = "Route"
            st.rerun()
    with c4:
        if st.button("🚨 SOS", key="nav_sos"):
            st.session_state.dashboard_view = "SOS"
            st.rerun()
    with c5:
        if st.button("⚙️ Account", key="nav_acc"):
            st.session_state.dashboard_view = "Account"
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
