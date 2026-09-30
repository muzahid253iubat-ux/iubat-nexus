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
    /* Main Background & Font Styling */
    .stApp {
        background-color: #0b1120;
        color: #ffffff;
    }
    
    /* Hide Streamlit Default Header/Footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Default (Laptop/PC View styling) */
    .mobile-bottom-nav {
        display: none; /* Hidden on PC */
    }

    /* Mobile / iPhone View Specific Styling (< 768px) */
    @media (max-width: 768px) {
        /* Hide PC bottom buttons if needed or reposition them */
        .pc-nav-container {
            display: none !important;
        }
        
        /* Show Mobile Bottom Navigation Bar (like Facebook app style) */
        .mobile-bottom-nav {
            display: flex;
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #1e293b;
            border-top: 1px solid #334155;
            justify-content: space-around;
            padding: 10px 0;
            z-index: 9999;
        }
        
        .mobile-nav-item {
            text-align: center;
            color: #94a3b8;
            font-size: 12px;
            text-decoration: none;
        }
        
        .mobile-nav-item i {
            font-size: 20px;
            display: block;
            margin-bottom: 2px;
        }
        
        /* Adjust padding at bottom so content doesn't hide behind mobile nav */
        .block-container {
            padding-bottom: 80px;
        }
    }
    </style>
""", unsafe_allow_html=True)

# --- USER PROFILE HEADER ---
st.markdown("""
    <div style="background-color: #1e293b; padding: 15px; border-radius: 12px; display: flex; align-items: center; justify-content: space-between; border: 1px solid #334155;">
        <div style="display: flex; align-items: center; gap: 15px;">
            <div style="font-size: 40px; background: #3b82f6; border-radius: 50%; width: 50px; height: 50px; display: flex; align-items: center; justify-content: center;">👨‍🎓</div>
            <div>
                <h3 style="margin: 0; color: #ffffff; font-size: 18px;">Abdullah Al Muzahid</h3>
                <p style="margin: 0; color: #94a3b8; font-size: 14px;">EEE</p>
            </div>
        </div>
        <div style="background: #ef4444; color: white; padding: 5px 12px; border-radius: 20px; font-size: 12px;">📍 Tongi</div>
    </div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- DASHBOARD CONTENT ---
st.markdown("### Shuttle Bus Schedule")
st.markdown("📅 Today Schedule")

# Bus Card
st.markdown("""
    <div style="background-color: #111827; padding: 20px; border-radius: 15px; border: 1px solid #1f2937;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-size: 16px; font-weight: bold; color: #60a5fa;">🚌 Bus 02</span>
            <span style="background-color: #7f1d1d; color: #fca5a5; padding: 3px 10px; border-radius: 10px; font-size: 12px;">Down Time</span>
        </div>
        <p style="color: #94a3b8; font-size: 13px; margin-top: 8px;">🚩 Route: Campus to Narshingdi</p>
        
        <div style="display: flex; justify-content: space-between; align-items: center; background: #1e293b; padding: 15px; border-radius: 10px; margin-top: 15px;">
            <div>
                <h2 style="margin: 0; color: #ffffff; font-size: 20px;">05:30 PM</h2>
                <p style="margin: 0; color: #94a3b8; font-size: 11px;">Departure • Campus</p>
            </div>
            <div style="font-size: 20px; color: #38bdf8;">➔</div>
            <div style="text-align: right;">
                <h2 style="margin: 0; color: #ffffff; font-size: 20px;">07:30 PM</h2>
                <p style="margin: 0; color: #94a3b8; font-size: 11px;">Arrival (ETA) • Velanagor</p>
            </div>
        </div>
        <p style="color: #94a3b8; font-size: 12px; margin-top: 12px;"><b>RouteMap:</b> Campus » Tongi Station Road » Amtoly Mor » T & T Bazar » Shilmoon</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# GPS Tracking Button
if st.button("🗺️ Launch Live GPS Tracking", use_container_width=True):
    st.success("GPS Tracking initiated...")

st.markdown("<br>", unsafe_allow_html=True)

# --- PC NAVIGATION BUTTONS (Visible on Laptop/PC) ---
st.markdown('<div class="pc-nav-container">', unsafe_allow_html=True)
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.button("🚌 Shuttle", use_container_width=True)
with col2:
    st.button("👩‍🏫 Faculty", use_container_width=True)
with col3:
    st.button("🗺️️ Route", use_container_width=True)
with col4:
    st.button("🚨 SOS", use_container_width=True)
with col5:
    st.button("⚙️ Account", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- MOBILE BOTTOM NAVIGATION BAR (Visible on Mobile/iPhone View) ---
st.markdown("""
    <div class="mobile-bottom-nav">
        <a href="#" class="mobile-nav-item" style="color: #38bdf8;">
            🏠<br>Home
        </a>
        <a href="#" class="mobile-nav-item">
            🚌<br>Shuttle
        </a>
        <a href="#" class="mobile-nav-item">
            🗺️<br>Route
        </a>
        <a href="#" class="mobile-nav-item">
            🚨<br>SOS
        </a>
        <a href="#" class="mobile-nav-item">
            ⚙️<br>Account
        </a>
    </div>
""", unsafe_allow_html=True)
