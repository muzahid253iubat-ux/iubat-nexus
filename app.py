import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="IUBAT Nexus - Smart Portal",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Responsiveness (Desktop vs Mobile View) and Styling
st.markdown("""
    <style>
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background-color: #0b0f19;
        color: #ffffff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Desktop View Container */
    .desktop-container {
        display: block;
    }
    
    /* Mobile View Container - hidden by default on large screens */
    .mobile-container {
        display: none;
    }

    /* Media Query for Mobile Devices (max-width: 768px) */
    @media only screen and (max-width: 768px) {
        .desktop-container {
            display: none !important;
        }
        .mobile-container {
            display: block !important;
        }
    }

    /* Common Card Styling */
    .dashboard-card {
        background-color: #111827;
        border: 1px solid #1f2937;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Session State Initialization for Authentication
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "Login"

# ==================== LOCKED FIRST PAGE (LOGIN / SIGNUP) ====================
def render_first_page():
    col1, col2, col3 = st.columns([1, 1.2, 1])
    
    with col2:
        st.markdown("<br><h1 style='text-align: center; color: #3b82f6;'>🎓 IUBAT Nexus</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #9ca3af;'>Smart Student Portal & Campus Companion</p><br>", unsafe_allow_html=True)
        
        # Tabs for Login & Register
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Create Account"])
        
        with tab1:
            st.markdown("### Welcome Back!")
            email = st.text_input("Email / Student ID", placeholder="Enter your ID or email", key="login_email")
            password = st.text_input("Password", type="password", placeholder="Enter password", key="login_pass")
            
            if st.button("Login to Portal", use_container_width=True, type="primary"):
                if email and password:
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.warning("Please fill in all fields.")
                    
        with tab2:
            st.markdown("### Register New Account")
            new_name = st.text_input("Full Name", placeholder="Abdullah Al Muzahid")
            new_email = st.text_input("Email / ID", placeholder="Enter email")
            new_pass = st.text_input("Password", type="password", placeholder="Create password")
            
            if st.button("Sign Up", use_container_width=True):
                if new_name and new_email and new_pass:
                    st.success("Account created successfully! Please login.")
                else:
                    st.warning("Please fill out all fields.")

# ==================== RESPONSIVE DASHBOARD ====================
def render_dashboard():
    # Top Bar with Profile and Logout Button
    top_col1, top_col2, top_col3 = st.columns([6, 2, 1])
    with top_col1:
        st.markdown("### 🚀 Welcome, Abdullah Al Muzahid")
        st.markdown("<span style='color: #9ca3af;'>EEE Department | Campus: Tongi</span>", unsafe_allow_html=True)
    with top_col3:
        if st.button("🚪 Logout", type="secondary", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

    st.markdown("---")

    # Responsive Layout Implementation using HTML/CSS Classes
    # Desktop View Layout (Matches Laptop Screenshot Style)
    st.markdown("""
        <div class="desktop-container">
            <div style="background-color: #111827; padding: 25px; border-radius: 12px; border: 1px solid #1f2937;">
                <h3 style="color: #60a5fa; margin-top: 0;">💻 Desktop / Laptop Dashboard View</h3>
                <p>This layout is optimized for wide screens, featuring multi-column widgets, side panels, and complete navigation panels just like your desktop setup.</p>
                <div style="display: flex; gap: 20px; margin-top: 15px;">
                    <div style="flex: 2; background: #1f2937; padding: 15px; border-radius: 8px;">
                        <h4>Shuttle Bus Schedule (Active)</h4>
                        <p><b>Bus 02</b> - Route: Campus to Narshingdi<br>Departure: 05:30 PM</p>
                    </div>
                    <div style="flex: 1; background: #1f2937; padding: 15px; border-radius: 8px;">
                        <h4>Quick Shortcuts</h4>
                        <p>• Shuttle<br>• Faculty<br>• SOS Emergency</p>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Mobile View Layout (Matches iPhone Screenshot Style)
    st.markdown("""
        <div class="mobile-container">
            <div style="background-color: #111827; padding: 15px; border-radius: 12px; border: 1px solid #1f2937;">
                <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #374151; padding-bottom: 10px; margin-bottom: 10px;">
                    <h3 style="color: #60a5fa; margin: 0;">📱 Mobile View</h3>
                    <span style="font-size: 20px;">☰</span>
                </div>
                <p style="font-size: 14px;">Optimized compact single-column view designed cleanly for smartphone screens.</p>
                <div style="background: #1f2937; padding: 12px; border-radius: 8px; margin-bottom: 10px;">
                    <h4 style="margin: 0 0 5px 0; font-size: 15px;">Shuttle Bus Schedule</h4>
                    <p style="font-size: 13px; margin: 0;">Bus 02 | 05:30 PM Departure</p>
                </div>
                <div style="background: #1f2937; padding: 12px; border-radius: 8px;">
                    <h4 style="margin: 0 0 5px 0; font-size: 15px;">Quick Navigation</h4>
                    <p style="font-size: 13px; margin: 0;">Shuttle | Faculty | SOS | Account</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# ==================== MAIN ROUTER ====================
if not st.session_state.logged_in:
    render_first_page()
else:
    render_dashboard()
