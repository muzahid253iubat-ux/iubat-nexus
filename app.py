import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="IUBAT Nexus - Portal",
    page_icon="🎓",
    layout="centered"
)

# Custom CSS for Unique Background & Styling
st.markdown("""
    <style>
    /* Main background with a stunning university campus vibe and dark gradient overlay */
    .stApp {
        background: linear-gradient(rgba(10, 25, 47, 0.85), rgba(10, 25, 47, 0.85)), 
                    url('https://images.unsplash.com/photo-1541339907198-e08756dedf3f?auto=format&fit=crop&w=1950&q=80');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    /* Glassmorphism Card Container for Login */
    .login-container {
        background: rgba(255, 255, 255, 0.08);
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        margin-top: 50px;
    }
    
    /* Text styling */
    h1, h2, h3, p, label {
        color: #ffffff !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Custom Button Styling */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #FF4B2B 0%, #FF416C 100%);
        color: white;
        font-weight: bold;
        border: none;
        padding: 12px;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(255, 75, 43, 0.4);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 75, 43, 0.6);
    }
    </style>
""", unsafe_allow_html=True)

# App Content Inside a Wrapper
st.markdown("<div class='login-container'>", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>🎓 IUBAT Nexus</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #cbd5e1;'>Your Smart University Companion Portal</p>", unsafe_allow_html=True)
st.write("")

# Login Form Elements
user_id = st.text_input("Student ID / Email", placeholder="e.g., 20103056")
password = st.text_input("Password", type="password", placeholder="••••••••")

st.write("")
if st.button("Secure Login"):
    if user_id and password:
        st.success(f"Welcome back, {user_id}! Redirecting to dashboard...")
    else:
        st.warning("Please enter both ID and password to continue.")

st.markdown("</div>", unsafe_allow_html=True)
