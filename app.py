import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="IUBAT Nexus - Smart Portal",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Facebook-like Theme and UI Styling
st.markdown("""
    <style>
    /* Main Background & Font */
    .stApp {
        background-color: #f0f2f5;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Top Navbar Styling */
    .fb-navbar {
        background-color: #ffffff;
        padding: 8px 16px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        display: flex;
        justify-content: space-between;
        align-items: center;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        z-index: 999;
    }
    
    /* Feed Card Styling */
    .fb-card {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 12px;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
    }
    
    /* Profile Header */
    .profile-header {
        background: linear-gradient(135deg, #1877f2, #0e5a14);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Session State Initialization for Login/Navigation
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ----------------- FIRST PAGE / LOGIN / FACEBOOK STYLE FEED -----------------
if not st.session_state.logged_in:
    # Top Mock Facebook Navbar
    st.markdown("""
        <div class="fb-navbar">
            <div style="font-size: 24px; font-weight: bold; color: #1877f2; display: flex; align-items: center;">
                facebook <span style="font-size: 12px; background: #e4e6eb; padding: 2px 6px; border-radius: 4px; margin-left: 8px; color: #050505;">Nexus</span>
            </div>
            <div style="font-size: 14px; color: #65676b; font-weight: 600;">
                IUBAT Smart Student Portal
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Layout with Feed Simulation on Left/Center and Login Sidebar on Right
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🌐 Campus Feed & Updates")
        
        # Simulated Post 1 (Like the university news in your screenshot)
        st.markdown("""
            <div class="fb-card">
                <div style="display: flex; align-items: center; margin-bottom: 8px;">
                    <div style="background: #1877f2; color: white; border-radius: 50%; width: 40px; height: 40px; display: flex; align-items: center; justify-content: font-weight: bold; margin-right: 10px;">I</div>
                    <div>
                        <b>IUBAT Official</b><br>
                        <span style="font-size: 12px; color: #65676b;">30 September, 2026 • 🌍</span>
                    </div>
                </div>
                <p>GreenMetric Ranking: Sustainable Higher Education Excellence at IUBAT. Proud to lead towards a greener campus!</p>
                <div style="background: #e4e6eb; height: 180px; border-radius: 6px; display: flex; align-items: center; justify-content: center; color: #65676b; font-weight: bold;">
                    [Campus GreenMetric Banner Preview]
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Simulated Post 2
        st.markdown("""
            <div class="fb-card">
                <div style="display: flex; align-items: center; margin-bottom: 8px;">
                    <div style="background: #2e7d32; color: white; border-radius: 50%; width: 40px; height: 40px; display: flex; align-items: center; justify-content: font-weight: bold; margin-right: 10px;">EN</div>
                    <div>
                        <b>EEE Department Club</b><br>
                        <span style="font-size: 12px; color: #65676b;">2 hours ago • ⚡</span>
                    </div>
                </div>
                <p>Arduino & MATLAB Simulink workshop registrations are now open for all fourth-semester students. Check your portal dashboard for details!</p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="fb-card" style="background: white; border: 1px solid #ddd; text-align: center;">
                <h3>Student Login</h3>
                <p style="font-size: 13px; color: #65676b;">Access your Shuttle, Routes, and Portal Dashboard</p>
            </div>
        """, unsafe_allow_html=True)
        
        student_id = st.text_input("Student ID / Email", placeholder="Enter your ID")
        password = st.text_input("Password", type="password", placeholder="Enter password")
        
        if st.button("Log In", type="primary", use_container_width=True):
            if student_id:
                st.session_state.logged_in = True
                st.session_state.student_id = student_id
                st.rerun()
            else:
                st.warning("Please enter your Student ID or credentials.")

# ----------------- DASHBOARD / MAIN APP AFTER LOGIN -----------------
else:
    # Profile Banner Header
    st.markdown("""
        <div class="profile-header">
            <h2>Abdullah Al Muzahid</h2>
            <p>EEE Undergraduate Student • IUBAT | 📍 Tongi, Gazipur</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🚌 Shuttle Bus Schedule & Live Tracker")
    
    # Shuttle Schedule Card (Matching your dashboard requirement)
    st.markdown("""
        <div style="background-color: #0b192c; padding: 20px; border-radius: 12px; color: white; border: 1px solid #1e293b;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h4>Bus 02</h4>
                <span style="background: #dc2626; padding: 2px 10px; border-radius: 12px; font-size: 12px;">Down Time</span>
            </div>
            <p style="color: #94a3b8; font-size: 14px;">Route: Campus to Narshingdi</p>
            <div style="display: flex; justify-content: space-between; margin-top: 15px; background: rgba(255,255,255,0.05); padding: 12px; border-radius: 8px;">
                <div>
                    <span style="font-size: 18px; font-weight: bold;">05:30 PM</span><br>
                    <span style="font-size: 12px; color: #94a3b8;">Departure • Campus</span>
                </div>
                <div style="font-size: 20px; align-self: center;">➔</div>
                <div>
                    <span style="font-size: 18px; font-weight: bold;">07:30 PM</span><br>
                    <span style="font-size: 12px; color: #94a3b8;">Arrival (ETA) • Velanagor</span>
                </div>
            </div>
            <p style="margin-top: 12px; font-size: 13px; color: #cbd5e1;"><b>RouteMap:</b> Campus » Tongi Station Road » Amtoly Mor » T & T Bazar » Shilmoon</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 Launch Live GPS Tracking", type="primary", use_container_width=True):
        st.success("GPS Tracking module activated! Real-time telemetry connected.")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("Log Out"):
        st.session_state.logged_in = False
        st.rerun()
