import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="IUBAT Nexus | Smart Portal",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Responsive Design (Laptop vs Mobile view matching your requirement), Secure Locked First Page, & Custom Dashboard
st.markdown("""
<style>
    /* Hide default Streamlit header and footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background-color: #0b0f19;
        color: #ffffff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* LOCKED FIRST PAGE (LOGIN / AUTH CONTAINER) */
    .auth-card {
        background: #111827;
        padding: 40px;
        border-radius: 20px;
        border: 1px solid #1f2937;
        box-shadow: 0 10px 25px rgba(0,0,0,0.5);
        max-width: 450px;
        margin: 80px auto;
        text-align: center;
    }

    /* RESPONSIVE DASHBOARD STYLING */
    /* Mobile View Optimization (iPhone Screen-like container when viewed on small screens) */
    @media (max-width: 768px) {
        .dashboard-container {
            max-width: 414px;
            margin: 0 auto;
            background: #0b0f19;
            border: 12px solid #1f2937;
            border-radius: 40px;
            padding: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.8);
            position: relative;
        }
        .desktop-only-banner {
            display: none !important;
        }
    }

    /* PC / Laptop View Optimization (Wide Screen 1st Image Layout) */
    @media (min-width: 769px) {
        .dashboard-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        .mobile-only-indicator {
            display: none !important;
        }
    }

    /* Profile Header Box */
    .profile-box {
        background: #111827;
        border: 1px solid #1f2937;
        padding: 20px;
        border-radius: 16px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 25px;
    }

    /* Card Box */
    .custom-card {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 16px;
        padding: 25px;
        margin-bottom: 20px;
    }

    /* Custom Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        font-weight: 600;
        padding: 0.6rem 1rem;
        transition: all 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State for Authentication (Locked First Page logic)
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'auth_mode' not in st.session_state:
    st.session_state.auth_mode = "Login"

# ==========================================
# LOCKED FIRST PAGE (LOGIN / SIGNUP)
# ==========================================
if not st.session_state.logged_in:
    st.markdown('<div class="auth-card">', unsafe_allow_html=True)
    st.markdown("<h2>🎓 IUBAT Nexus</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #9ca3af;'>Your Smart Student Portal</p>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔑 Login", "📝 Create Account"])
    
    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)
        login_id = st.text_input("Student ID / Email", placeholder="Enter your ID")
        login_pass = st.text_input("Password", type="password", placeholder="Enter password")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Log In", type="primary"):
            if login_id and login_pass:
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Please enter valid credentials!")
                
    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)
        new_name = st.text_input("Full Name", placeholder="Abdullah Al Muzahid")
        new_id = st.text_input("Student ID", placeholder="e.g. 22103056")
        new_pass = st.text_input("New Password", type="password", placeholder="Create password")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Register Account", type="success"):
            if new_name and new_id and new_pass:
                st.success("Account created successfully! Please log in.")
            else:
                st.error("Please fill all fields!")
                
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# RESPONSIVE DASHBOARD (PC vs MOBILE VIEW)
# ==========================================
else:
    st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
    
    # Top Profile & Logout Section
    col_p1, col_p2 = st.columns([4, 1])
    with col_p1:
        st.markdown("""
            <div style="display: flex; align-items: center; gap: 15px;">
                <div style="background: #3b82f6; width: 50px; height: 50px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 20px;">AM</div>
                <div>
                    <h3 style="margin: 0; font-size: 18px;">Abdullah Al Muzahid</h3>
                    <p style="margin: 0; color: #9ca3af; font-size: 14px;">EEE | Tongi</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
    with col_p2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚪 Logout", type="secondary"):
            st.session_state.logged_in = False
            st.rerun()

    st.markdown("---")
    
    # Responsive Mode Indicator & Dashboard Content
    st.markdown("""
        <div class="desktop-only-banner" style="background: #1e293b; padding: 10px 15px; border-radius: 8px; margin-bottom: 15px; font-size: 13px; color: #38bdf8;">
            💻 <b>Laptop/PC View Active:</b> Optimized with wide screen layout (matching your Laptop screenshot style).
        </div>
        <div class="mobile-only-indicator" style="background: #1e293b; padding: 10px 15px; border-radius: 8px; margin-bottom: 15px; font-size: 13px; color: #34d399;">
            📱 <b>Mobile View Active:</b> Optimized inside a mobile frame layout (matching your iPhone screenshot style).
        </div>
    """, unsafe_allow_html=True)

    # Main Dashboard Widgets (Shuttle Schedule & Quick Links)
    st.markdown("### 🚍 Shuttle Bus Schedule")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
            <div class="custom-card">
                <span style="background: #ef4444; color: white; padding: 2px 8px; border-radius: 6px; font-size: 12px;">Down Time</span>
                <h4 style="margin-top: 10px;">Bus 02 (Campus to Narshingdi)</h4>
                <p style="color: #9ca3af; font-size: 14px;">Departure: 05:30 PM &nbsp;➔&nbsp; Arrival: 07:30 PM</p>
                <p style="font-size: 13px; color: #cbd5e1;"><b>RouteMap:</b> Campus ➔ Tongi Station Road ➔ Amtoly Mor</p>
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
            <div class="custom-card">
                <span style="background: #10b981; color: white; padding: 2px 8px; border-radius: 6px; font-size: 12px;">Active</span>
                <h4 style="margin-top: 10px;">Bus 01 (Uttara to Campus)</h4>
                <p style="color: #9ca3af; font-size: 14px;">Departure: 08:00 AM &nbsp;➔&nbsp; Arrival: 08:45 AM</p>
                <p style="font-size: 13px; color: #cbd5e1;"><b>RouteMap:</b> House Building ➔ Azampur ➔ Campus</p>
            </div>
        """, unsafe_allow_html=True)

    if st.button("📍 Launch Live GPS Tracking", type="primary"):
        st.info("Live tracking module initialized...")

    # Bottom Navigation / Quick Action Bar
    st.markdown("<br>", unsafe_allow_html=True)
    nav_cols = st.columns(5)
    with nav_cols[0]:
        st.button("🚌 Shuttle")
    with nav_cols[1]:
        st.button("👨‍🏫 Faculty")
    with nav_cols[2]:
        st.button("🗺️ Route")
    with nav_cols[3]:
        st.button("🚨 SOS")
    with nav_cols[4]:
        st.button("⚙️ Account")

    st.markdown('</div>', unsafe_allow_html=True)
