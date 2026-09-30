import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="IUBAT Nexus - Smart Portal",
    page_icon="🎓",
    layout="wide"
)

# Custom CSS for Responsive Design (Laptop vs iPhone/Mobile View)
st.markdown("""
    <style>
    .stApp {
        background-color: #0b1120;
        color: #ffffff;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Mobile Bottom Navigation Bar (Hidden by default on PC) */
    .mobile-bottom-nav {
        display: none;
    }

    /* Media Query for Mobile / iPhone View (< 768px) */
    @media (max-width: 768px) {
        /* Hide the entire PC navigation section using stElement selector or direct layout */
        div[data-testid="column"] {
            width: 100% !important;
            flex: 100% !important;
            min-width: 100% !important;
        }
        
        /* Specifically target the PC nav buttons container by hiding element with buttons */
        .pc-nav-area {
            display: none !important;
        }
        
        /* Show Mobile Bottom Navigation Bar */
        .mobile-bottom-nav {
            display: flex !important;
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #1e293b;
            border-top: 1px solid #334155;
            justify-content: space-around;
            padding: 12px 0;
            z-index: 99999;
        }
        
        .mobile-nav-item {
            text-align: center;
            color: #94a3b8;
            font-size: 11px;
            text-decoration: none;
            font-weight: 500;
        }
        
        .mobile-nav-item:hover, .mobile-nav-item.active {
            color: #38bdf8;
        }
        
        /* Add bottom padding to body so content isn't hidden behind the fixed bar */
        .block-container {
            padding-bottom: 90px !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

# --- USER PROFILE HEADER ---
st.markdown("""
    <div style="background-color: #1e293b; padding: 15px; border-radius: 12px; display: flex; align-items: center; justify-content: space-between; border: 1px solid #334155;">
        <div style="display: flex; align-items: center; gap: 15px;">
            <div style="font-size: 30px; background: #3b82f6; border-radius: 50%; width: 45px; height: 45px; display: flex; align-items: center; justify-content: center;">👨‍🎓</div>
            <div>
                <h3 style="margin: 0; color: #ffffff; font-size: 18px;">Abdullah Al Muzahid</h3>
                <p style="margin: 0; color: #94a3b8; font-size: 14px;">EEE</p>
            </div>
        </div>
        <div style="background: #ef4444; color: white; padding: 5px 12px; border-radius: 20px; font-size: 12px;">📍 Tongi</div>
    </div>
""", unsafe_allow_html=True)

st.write("")

# --- DASHBOARD CONTENT ---
st.markdown("### Shuttle Bus Schedule")
st.markdown("📅 Today Schedule")

# Bus Card Container
with st.container():
    st.markdown("""
        <div style="background-color: #111827; padding: 20px; border-radius: 15px; border: 1px solid #1f2937;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 16px; font-weight: bold; color: #60a5fa;">🚌 Bus 02</span>
                <span style="background-color: #7f1d1d; color: #fca5a5; padding: 3px 10px; border-radius: 10px; font-size: 12px;">Down Time</span>
            </div>
            <p style="color: #94a3b8; font-size: 13px; margin-top: 8px;">🚩 Route: Campus to Narshingdi</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Inner schedule timing row
    sc1, sc2, sc3 = st.columns([3, 1, 3])
    with sc1:
        st.markdown("<h2 style='margin:0; font-size:22px; color:#ffffff;'>05:30 PM</h2>", unsafe_allow_html=True)
        st.markdown("<p style='margin:0; font-size:11px; color:#94a3b8;'>Departure • Campus</p>", unsafe_allow_html=True)
    with sc2:
        st.markdown("<h2 style='text-align:center; color:#38bdf8; margin:0;'>➔</h2>", unsafe_allow_html=True)
    with sc3:
        st.markdown("<h2 style='margin:0; font-size:22px; color:#ffffff; text-align:right;'>07:30 PM</h2>", unsafe_allow_html=True)
        st.markdown("<p style='margin:0; font-size:11px; color:#94a3b8; text-align:right;'>Arrival (ETA) • Velanagor</p>", unsafe_allow_html=True)
        
    st.markdown("""
        <p style="color: #94a3b8; font-size: 12px; margin-top: 15px;"><b>RouteMap:</b> Campus » Tongi Station Road » Amtoly Mor » T & T Bazar » Shilmoon</p>
    """, unsafe_allow_html=True)

st.write("")

# GPS Tracking Button
if st.button("🗺️ Launch Live GPS Tracking", use_container_width=True):
    st.success("GPS Tracking initiated...")

st.write("")

# --- PC NAVIGATION BUTTONS (Wrapped in a special div to hide on mobile) ---
st.markdown('<div class="pc-nav-area">', unsafe_allow_html=True)
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.button("🚌 Shuttle", use_container_width=True, key="pc_btn_1")
with col2:
    st.button("👩‍🏫 Faculty", use_container_width=True, key="pc_btn_2")
with col3:
    st.button("🗺 Route", use_container_width=True, key="pc_btn_3")
with col4:
    st.button("🚨 SOS", use_container_width=True, key="pc_btn_4")
with col5:
    st.button("⚙ Account", use_container_width=True, key="pc_btn_5")
st.markdown('</div>', unsafe_allow_html=True)

# --- MOBILE BOTTOM NAVIGATION BAR (Visible ONLY on Mobile/iPhone) ---
st.markdown("""
    <div class="mobile-bottom-nav">
        <a href="#" class="mobile-nav-item active">🏠<br>Home</a>
        <a href="#" class="mobile-nav-item">🚌<br>Shuttle</a>
        <a href="#" class="mobile-nav-item">🗺️<br>Route</a>
        <a href="#" class="mobile-nav-item">🚨<br>SOS</a>
        <a href="#" class="mobile-nav-item">⚙️<br>Account</a>
    </div>
""", unsafe_allow_html=True)
