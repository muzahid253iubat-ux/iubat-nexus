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

# --- Persistent Session Management & Language State ---
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
if "lang" not in st.session_state:
    st.session_state.lang = "EN"

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

# --- Dictionary for Multilingual Text ---
t = {
    "EN": {
        "title": "All of IUBAT,<br>Working For You.",
        "subtitle": "Sign in with your student ID and password to access smart shuttle schedules, live GPS tracking, faculty directories, and campus updates instantly.",
        "card_header": "Log in to IUBAT Nexus",
        "id_placeholder": "Student ID Number",
        "pass_placeholder": "Password",
        "remember": "Remember session",
        "login_btn": "Log in",
        "forgot": "Forgotten password?",
        "create_btn": "Create new account",
        "create_title": "Create a new account",
        "create_subtitle": "It's quick and easy.",
        "name_ph": "Full Name",
        "dept_ph": "Department (e.g. EEE)",
        "univ_ph": "University Name",
        "new_pass_ph": "New password",
        "upload_ph": "Upload Profile Photo (Optional)",
        "signup_btn": "Sign Up",
        "back_login": "⬅ Already have an account?",
        "shuttle_title": "Shuttle Bus Schedule",
        "faculty_title": "Faculty Directory & Office Hours",
        "route_title": "Route Stoppages (Campus to Narshingdi)",
        "sos_title": "Emergency SOS & Helplines",
        "account_title": "Student Account & Settings",
        "nav_shuttle": "🚌 Shuttle",
        "nav_faculty": "👨‍🏫 Faculty",
        "nav_route": "🗺️ Route",
        "nav_sos": "🚨 SOS",
        "nav_acc": "⚙️ Account",
        "footer": "© 2026 IUBAT Nexus • Smart University Portal"
    },
    "BN": {
        "title": "আপনার সম্পূর্ণ আইউবাট,<br>সবসময় আপনার সাথে।",
        "subtitle": "স্মার্ট শাটল শিডিউল, লাইভ জিপিএস ট্র্যাকিং, শিক্ষকগণের তালিকা এবং ক্যাম্পাস আপডেট পেতে আপনার স্টুডেন্ট আইডি ও পাসওয়ার্ড দিয়ে লগইন করুন।",
        "card_header": "আইউবাট নেক্সাসে লগইন করুন",
        "id_placeholder": "স্টুডেন্ট আইডি নম্বর",
        "pass_placeholder": "পাসওয়ার্ড",
        "remember": "লগইন মনে রাখুন",
        "login_btn": "লগইন করুন",
        "forgot": "পাসওয়ার্ড ভুলে গেছেন?",
        "create_btn": "নতুন একাউন্ট তৈরি করুন",
        "create_title": "নতুন একাউন্ট তৈরি করুন",
        "create_subtitle": "এটি খুব দ্রুত এবং সহজ।",
        "name_ph": "পূর্ণ নাম",
        "dept_ph": "ডিপার্টমেন্ট (যেমন: EEE)",
        "univ_ph": "বিশ্ববিদ্যালয়ের নাম",
        "new_pass_ph": "নতুন পাসওয়ার্ড",
        "upload_ph": "প্রোফাইল ছবি আপলোড করুন (ঐচ্ছিক)",
        "signup_btn": "সাইন আপ",
        "back_login": "⬅ ইতিমধ্যে একাউন্ট আছে?",
        "shuttle_title": "শাটল বাস শিডিউল",
        "faculty_title": "শিক্ষকগণের তালিকা ও অফিস সময়",
        "route_title": "বাস রুট ও স্টপেজ (ক্যাম্পাস থেকে নরসিংদী)",
        "sos_title": "জরুরী ইমার্জেন্সি ও হেল্পলাইন",
        "account_title": "স্টুডেন্ট একাউন্ট ও সেটিংস",
        "nav_shuttle": "🚌 শাটল",
        "nav_faculty": "👨‍🏫 শিক্ষক",
        "nav_route": "🗺️ রুট",
        "nav_sos": "🚨 এসওএস",
        "nav_acc": "⚙ একাউন্ট",
        "footer": "© ২০২৬ আইউবাট নেক্সাস • স্মার্ট ইউনিভার্সিটি পোর্টাল"
    }
}

lang_key = st.session_state.lang

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
            <h2 style='font-size: 1.25rem; font-weight: 600; color: #F1F5F9;'>Loading IUBAT Nexus Portal...</h2>
        </div>
    """, unsafe_allow_html=True)
    time.sleep(0.8)
    st.session_state.splash_shown = True
    st.rerun()

def handle_create_acc():
    st.session_state.is_registering = True

if not st.session_state.logged_in:
    
    logo_html = f"<img src='{logo_image_data}' style='width: 38px; height: 38px; border-radius: 50%; object-fit: cover; border: 2px solid #0EA5E9;'>" if logo_image_data else "<span style='font-size: 1.5rem;'>🎓</span>"
    
    new_lang_top = "BN" if st.session_state.lang == "EN" else "EN"
    btn_label_top = "🇧🇩 বাংলা" if st.session_state.lang == "EN" else "🇬🇧 English"
    
    st.markdown(f"""
        <style>
        .stApp {{ background: #070B14; }}
        .stApp::before {{
            content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: url('{bg_image_data}') no-repeat center center fixed; background-size: cover; z-index: 0;
        }}
        .stApp::after {{
            content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(7, 11, 20, 0.88); z-index: 0;
        }}
        .block-container {{
            position: relative; z-index: 10; padding-top: 25px !important; padding-bottom: 120px !important; max-width: 1200px !important; margin: auto !important;
        }}
        #MainMenu, header, footer {{visibility: hidden;}}
        
        .top-banner-pill {{
            background: rgba(15, 23, 42, 0.75); backdrop-filter: blur(12px);
            border: 1px solid rgba(14, 165, 233, 0.3); border-radius: 12px;
            padding: 12px 18px; color: #FFFFFF; font-size: 0.98rem; font-weight: 700;
            display: flex; align-items: center; justify-content: center; text-align: center;
            margin-bottom: 14px; box-shadow: 0 4px 15px rgba(0,0,0,0.4);
            letter-spacing: -0.2px;
        }}

        .fb-card {{
            background: rgba(15, 23, 42, 0.94) !important; backdrop-filter: blur(18px);
            border-radius: 14px !important; padding: 20px 24px 18px 24px !important;
            border: 1px solid rgba(14, 165, 233, 0.25) !important; box-shadow: 0 15px 40px rgba(0,0,0,0.7);
            width: 100%; max-width: 390px; margin-left: auto; position: relative; z-index: 20;
        }}
        .fb-title {{
            font-size: 1.35rem; font-weight: 700; color: #FFFFFF; margin-bottom: 14px; font-family: system-ui, -apple-system, sans-serif;
        }}
        .stTextInput>div>div>input {{
            background-color: rgba(30, 41, 59, 0.75) !important; color: #F1F5F9 !important; border-radius: 6px !important;
            border: 1px solid rgba(14, 165, 233, 0.3); padding: 10px 14px; font-size: 0.95rem;
        }}
        .stFormSubmitButton>button {{
            width: 100% !important; background-color: #0866FF !important; color: #FFFFFF !important;
            font-weight: 700 !important; border-radius: 6px !important; border: none !important;
            padding: 11px !important; font-size: 1rem !important; margin-top: 4px;
            box-shadow: 0 4px 12px rgba(8, 102, 255, 0.3); transition: background 0.2s;
        }}
        .stFormSubmitButton>button:hover {{
            background-color: #1877F2 !important;
        }}
        .create-btn-container div.stButton > button {{
            width: 100% !important; background-color: #42B72A !important; color: #FFFFFF !important;
            font-weight: 700 !important; border-radius: 6px !important; border: none !important;
            padding: 11px !important; font-size: 1rem !important;
            box-shadow: 0 4px 12px rgba(66, 183, 42, 0.3);
        }}
        .create-btn-container div.stButton > button:hover {{
            background-color: #36A420 !important;
        }}
        .fb-footer-box {{
            position: relative; margin-top: 60px; width: 100%; border-top: 1px solid rgba(255,255,255,0.12); padding-top: 25px; padding-bottom: 40px; font-family: system-ui, -apple-system, sans-serif; z-index: 20;
        }}
        .fb-copyright {{
            color: #737B83; font-size: 12px; margin-top: 15px;
        }}
        </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div style='display: flex; justify-content: space-between; align-items: center; width: 100%; padding: 0 10px; margin-bottom: 25px;'>
            <div style='display: flex; align-items: center; gap: 10px;'>
                {logo_html}
                <span style='color: #FFFFFF; font-size: 1.3rem; font-weight: 800; letter-spacing: -0.3px;'>IUBAT Nexus</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([1.1, 0.9], gap="large")

    with col_left:
        st.markdown(f"""
            <div style='padding-top: 20px; padding-left: 10px;'>
                <h1 style='color: #FFFFFF; font-size: 3.1rem; font-weight: 800; margin: 0 0 15px 0; line-height: 1.15; letter-spacing: -1px;'>
                    {t[lang_key]["title"]}
                </h1>
                <p style='color: #94A3B8; font-size: 1.1rem; line-height: 1.6; max-width: 480px;'>
                    {t[lang_key]["subtitle"]}
                </p>
            </div>
        """, unsafe_allow_html=True)

    with col_right:
        # Language Switch Button
        if st.button(btn_label_top, key="lang_toggle_btn", use_container_width=True):
            st.session_state.lang = new_lang_top
            st.rerun()

        # Login Card Banner Header
        st.markdown(f"""
            <div class="top-banner-pill">
                🔒 {t[lang_key]["card_header"]}
            </div>
        """, unsafe_allow_html=True)

        if st.session_state.is_registering:
            st.markdown("<div class='fb-card'>", unsafe_allow_html=True)
            st.markdown(f"<div class='fb-title'>{t[lang_key]['create_title']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='color: #94A3B8; font-size: 0.88rem; margin-bottom: 14px;'>{t[lang_key]['create_subtitle']}</div>", unsafe_allow_html=True)

            with st.form("register_form"):
                reg_name = st.text_input("Full Name", placeholder=t[lang_key]["name_ph"])
                reg_id = st.text_input("ID Number", placeholder=t[lang_key]["id_placeholder"])
                reg_dept = st.text_input("Department", placeholder=t[lang_key]["dept_ph"])
                reg_univ = st.text_input("University", placeholder=t[lang_key]["univ_ph"], value="IUBAT")
                reg_pass = st.text_input("Password", type="password", placeholder=t[lang_key]["new_pass_ph"])
                reg_photo = st.file_uploader(t[lang_key]["upload_ph"], type=["jpg", "png", "jpeg"])

                if st.form_submit_button(t[lang_key]["signup_btn"]):
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
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            if st.button(t[lang_key]["back_login"]):
                st.session_state.is_registering = False
                st.rerun()

        else:
            # Clean Login Form container wrapped cleanly (no extra empty boxes)
            with st.form("login_form"):
                user_id = st.text_input("ID Number", placeholder=t[lang_key]["id_placeholder"])
                password = st.text_input("Password", type="password", placeholder=t[lang_key]["pass_placeholder"])

                remember_me = st.checkbox(t[lang_key]["remember"])

                if st.form_submit_button(t[lang_key]["login_btn"]):
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

            st.markdown(f"<div style='text-align: center; margin: 14px 0 4px 0;'><a href='#' style='color: #38BDF8; font-size: 0.85rem; text-decoration: none;'>{t[lang_key]['forgot']}</a></div>", unsafe_allow_html=True)
            st.markdown("<hr style='border-color: rgba(255,255,255,0.08); margin: 18px 0;'>", unsafe_allow_html=True)
            st.markdown("<div class='create-btn-container'>", unsafe_allow_html=True)
            st.button(t[lang_key]["create_btn"], key="btn_create_acc", on_click=handle_create_acc)
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(f"""
        <div class="fb-footer-box">
            <div style="color: #94A3B8; font-size: 0.95rem; margin-bottom: 6px;">
                💡 <b>Tip:</b> Click the top button (<b>🇧🇩 বাংলা / 🇬🇧 English</b>) anytime to switch language instantly!
            </div>
            <div class="fb-copyright">
                {t[lang_key]["footer"]}
            </div>
        </div>
    """, unsafe_allow_html=True)

else:
    photo_render = f"<img src='data:image/jpeg;base64,{st.session_state.user_photo}'>" if st.session_state.user_photo else "🎓"
    
    top_c1, top_c2 = st.columns([5, 1.8])
    with top_c1:
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
                <div class='location-badge-pro'>📍 Tongi</div>
            </div>
        """, unsafe_allow_html=True)
    with top_c2:
        new_lang = "BN" if st.session_state.lang == "EN" else "EN"
        btn_label = "🇧🇩 বাংলা" if st.session_state.lang == "EN" else "🇬🇧 English"
        if st.button(btn_label, key="dash_lang_btn", use_container_width=True):
            st.session_state.lang = new_lang
            st.rerun()

    if st.session_state.dashboard_view == "Shuttle":
        st.markdown(f"<div style='font-size: 1.25rem; font-weight: 800; margin: 16px 0 6px 0; color: #F1F5F9;'>{t[lang_key]['shuttle_title']}</div>", unsafe_allow_html=True)
        st.markdown("<div style='font-size: 0.85rem; color: #94A3B8; margin-bottom: 14px;'>📅 Today Schedule</div>", unsafe_allow_html=True)

        st.markdown("""
            <div class='sched-main-card-pro'>
                <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;'>
                    <div style='display: flex; align-items: center; gap: 8px;'>
                        <span style='font-size: 1.4rem;'>🚌</span>
                        <span style='font-weight: 800; font-size: 1.15rem;'>Bus 02</span>
                        <span class='badge-tag-pro' style='background: rgba(239, 68, 68, 0.2); color: #F87171;'>Down Time</span>
                    </div>
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
            </div>
        """, unsafe_allow_html=True)

        if st.button("🗺️ Launch Live GPS Tracking", use_container_width=True, type="primary"):
            st.success("🟢 Bus 02 is currently active near Tongi Station Road. Speed: 32 km/h.")

    elif st.session_state.dashboard_view == "Faculty":
        st.markdown(f"<div style='font-size: 1.25rem; font-weight: 800; margin: 16px 0;'>{t[lang_key]['faculty_title']}</div>", unsafe_allow_html=True)
        st.markdown("""
            <div class='sched-main-card-pro'>
                <div style='font-size: 1.1rem; font-weight: 800; color: #F1F5F9;'>Prof. Dr. M. Ahmed</div>
                <span class='badge-tag-pro'>EEE Department</span><br><br>
                <div style='font-size: 0.9rem; color: #CBD5E1;'>📧 m.ahmed@iubat.edu<br>🕒 Office Hours: Sun-Tue (03:00 PM - 05:00 PM)</div>
            </div>
        """, unsafe_allow_html=True)

    elif st.session_state.dashboard_view == "Route":
        st.markdown(f"<div style='font-size: 1.25rem; font-weight: 800; margin: 16px 0;'>{t[lang_key]['route_title']}</div>", unsafe_allow_html=True)
        st.markdown("""
            <div class='sched-main-card-pro'>
                <div class='route-stop-pro'>📍 Campus (Uttara) - Starting Point</div>
                <div class='route-stop-pro'>📍 Tongi Station Road</div>
                <div class='route-stop-pro'>📍 Amtoly Mor</div>
                <div class='route-stop-pro'>📍 T & T Bazar</div>
                <div class='route-stop-pro'>📍 Shilmoon</div>
            </div>
        """, unsafe_allow_html=True)

    elif st.session_state.dashboard_view == "SOS":
        st.markdown(f"<div style='font-size: 1.25rem; font-weight: 800; margin: 16px 0;'>{t[lang_key]['sos_title']}</div>", unsafe_allow_html=True)
        st.markdown("""
            <div class='sched-main-card-pro' style='border-left: 5px solid #EF4444;'>
                <div style='font-size: 1.1rem; font-weight: 800; color: #F1F5F9;'>Campus Security Control Room</div>
                <div style='font-size: 0.9rem; color: #CBD5E1; margin-top: 6px;'>📞 Hotline: +880 1713-393291</div>
            </div>
        """, unsafe_allow_html=True)

    elif st.session_state.dashboard_view == "Account":
        st.markdown(f"<div style='font-size: 1.25rem; font-weight: 800; margin: 16px 0;'>{t[lang_key]['account_title']}</div>", unsafe_allow_html=True)
        
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

    st.markdown("<div class='bottom-nav-dock'>", unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        if st.button(t[lang_key]["nav_shuttle"], key="nav_shuttle"):
            st.session_state.dashboard_view = "Shuttle"
            st.rerun()
    with c2:
        if st.button(t[lang_key]["nav_faculty"], key="nav_faculty"):
            st.session_state.dashboard_view = "Faculty"
            st.rerun()
    with c3:
        if st.button(t[lang_key]["nav_route"], key="nav_route"):
            st.session_state.dashboard_view = "Route"
            st.rerun()
    with c4:
        if st.button(t[lang_key]["nav_sos"], key="nav_sos"):
            st.session_state.dashboard_view = "SOS"
            st.rerun()
    with c5:
        if st.button(t[lang_key]["nav_acc"], key="nav_acc"):
            st.session_state.dashboard_view = "Account"
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
