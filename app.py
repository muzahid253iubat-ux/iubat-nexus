import streamlit as st

# Page configuration
st.set_page_config(
    page_title="IUBAT Nexus - Smart Portal",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Initialize session state for authentication
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "page" not in st.session_state:
    st.session_state.page = "login"

# Custom CSS for Responsive Design (Desktop vs Mobile Frame & Custom Styling)
st.markdown(
    """
    <style>
        /* Hide default Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        .stApp {
            background-color: #0b0f19;
            color: #ffffff;
            font-family: 'Inter', sans-serif;
        }

        /* Responsive Wrapper: Simulates iPhone view on mobile or narrow screens, Full view on Desktop */
        @media screen and (max-width: 768px) {
            .main .block-container {
                max-width: 420px !important;
                margin: auto !important;
                padding: 15px !important;
                background-color: #0b0f19;
                border: 4px solid #2d3748;
                border-radius: 35px;
                box-shadow: 0px 10px 30px rgba(0,0,0,0.8);
                margin-top: 20px;
                margin-bottom: 20px;
            }
        }
        
        @media screen and (min-width: 769px) {
            .main .block-container {
                max-width: 1200px !important;
                padding: 30px !important;
            }
        }

        /* Card styling */
        .dashboard-card {
            background-color: #111827;
            border: 1px solid #1f2937;
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- LOGIN / FIRST PAGE ---
if not st.session_state.logged_in:
  st.markdown(
      "<h1 style='text-align: center; color: #3b82f6;'>IUBAT Nexus</h1>",
      unsafe_allow_html=True,
  )
  st.markdown(
      "<p style='text-align: center; color: #9ca3af;'>Please login to your"
      " account</p>",
      unsafe_allow_html=True,
  )

  col1, col2, col3 = st.columns([1, 2, 1])
  with col2:
    with st.form("login_form"):
      username = st.text_input("Username / Student ID")
      password = st.text_input("Password", type="password")
      submit = st.form_submit_button("Login", use_container_width=True)

      if submit:
        # Simple validation check for demo
        if username and password:
          st.session_state.logged_in = True
          st.session_state.page = "dashboard"
          st.rerun()
        else:
          st.error("Please enter credentials!")

# --- DASHBOARD PAGE ---
else:
  # Top Bar with Logout Button to check First Page easily
  top_col1, top_col2 = st.columns([8, 2])
  with top_col1:
    st.markdown("### 🎓 IUBAT Portal Dashboard")
  with top_col2:
    if st.button("🚪 Logout", use_container_width=True):
      st.session_state.logged_in = False
      st.session_state.page = "login"
      st.rerun()

  st.markdown("---")

  # User Profile Header Section (Matches image style)
  st.markdown(
      """
        <div style="background-color: #111827; border: 1px solid #1f2937; border-radius: 12px; padding: 15px; display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px;">
            <div style="display: flex; align-items: center; gap: 15px;">
                <div style="background-color: #3b82f6; color: white; border-radius: 50%; width: 50px; height: 50px; display: flex; align-items: center; justify-content: center; font-size: 20px; font-weight: bold;">AM</div>
                <div>
                    <h4 style="margin: 0; color: #ffffff;">Abdullah Al Muzahid</h4>
                    <p style="margin: 0; color: #9ca3af; font-size: 14px;">EEE • Tongi</p>
                </div>
            </div>
            <div>
                <span style="background-color: #1e3a8a; color: #93c5fd; padding: 5px 12px; border-radius: 20px; font-size: 12px;">BD বাংলা</span>
            </div>
        </div>
    """,
      unsafe_allow_html=True,
  )

  # Shuttle Bus Schedule Section (As seen in your dashboard screenshot)
  st.markdown("### Shuttle Bus Schedule")
  st.markdown(
      '<p style="color: #9ca3af; font-size: 13px;">📅 Today Schedule</p>',
      unsafe_allow_html=True,
  )

  st.markdown(
      """
        <div style="background-color: #0f172a; border: 1px solid #1e293b; border-radius: 15px; padding: 20px; margin-bottom: 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <span style="font-weight: bold; font-size: 16px;">🚌 Bus 02</span>
                <span style="background-color: #7f1d1d; color: #fca5a5; padding: 2px 10px; border-radius: 10px; font-size: 12px;">Down Time</span>
            </div>
            <p style="color: #9ca3af; font-size: 13px; margin-bottom: 15px;">🏁 Route: Campus to Narshingdi</p>
            
            <div style="display: flex; justify-content: space-between; align-items: center; background-color: #111827; padding: 15px; border-radius: 10px;">
                <div>
                    <h3 style="margin: 0; color: #ffffff;">05:30 PM</h3>
                    <p style="margin: 0; color: #9ca3af; font-size: 12px;">Departure • Campus</p>
                </div>
                <div style="color: #3b82f6; font-size: 24px;">➔</div>
                <div style="text-align: right;">
                    <h3 style="margin: 0; color: #ffffff;">07:30 PM</h3>
                    <p style="margin: 0; color: #9ca3af; font-size: 12px;">Arrival (ETA) • Velanagor</p>
                </div>
            </div>
            <p style="color: #9ca3af; font-size: 12px; margin-top: 15px;"><b>RouteMap:</b> Campus » Tongi Station Road » Amtoly Mor » T & T Bazar » Shilmoon</p>
        </div>
    """,
      unsafe_allow_html=True,
  )

  # Launch GPS Button
  if st.button("📖 Launch Live GPS Tracking", use_container_width=True):
    st.info("GPS Tracking feature is launching...")

  # Bottom Navigation Menu Icons
  st.markdown("<br>", unsafe_allow_html=True)
  col_n1, col_n2, col_n3, col_n4, col_n5 = st.columns(5)
  with col_n1:
    st.button("🚌 Shuttle", use_container_width=True)
  with col_n2:
    st.button("👨‍🏫 Faculty", use_container_width=True)
  with col_n3:
    st.button("🗺️ Route", use_container_width=True)
  with col_n4:
    st.button("🚨 SOS", use_container_width=True)
  with col_n5:
    st.button("⚙️ Account", use_container_width=True)
