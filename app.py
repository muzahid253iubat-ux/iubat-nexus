import streamlit as st

# --- App Setup ---
st.set_page_config(
    page_title="IUBAT Nexus | Portal",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS for Stunning Background & Glassmorphism ---
st.markdown("""
    <style>
    /* Stunning University Background using High-Quality Image with Dark Overlay */
    .stApp {
        background: linear-gradient(rgba(10, 25, 47, 0.8), rgba(10, 25, 47, 0.85)), 
                    url('https://images.unsplash.com/photo-1541339907198-e08756dedf3f?auto=format&fit=crop&w=1950&q=80');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    /* Glassmorphism Login Container */
    .login-container {
        background: rgba(255, 255, 255, 0.07);
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        margin-top: 5vh;
        max-width: 450px;
        margin-left: auto;
        margin-right: auto;
    }
    
    /* Text Styling */
    h1, h2, h3, p, label {
        color: #ffffff !important;
        text-align: center;
        font-family: 'Inter', sans-serif;
    }
    
    /* Input Fields */
    .stTextInput>div>div>input {
        background-color: rgba(255, 255, 255, 0.12);
        color: white;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Login Button */
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
    
    /* Footer */
    .footer {
        position: fixed;
        left: 0;
        bottom: 15px;
        width: 100%;
        text-align: center;
        color: rgba(255, 255, 255, 0.6);
        font-size: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Main Login UI ---
st.markdown("<h1>🎓 IUBAT Nexus</h1>", unsafe_allow_html=True)
st.markdown("<p>Your Smart University Companion Portal</p>", unsafe_allow_html=True)
st.write("")

with st.container():
    st.markdown("<div class='login-container'>", unsafe_allow_html=True)
    st.markdown("<h3>Portal Sign In</h3>", unsafe_allow_html=True)
    
    user_id = st.text_input("Student ID / Email", placeholder="e.g., 20103056")
    password = st.text_input("Password", type="password", placeholder="••••••••")
    
    st.write("")
    if st.button("Secure Login"):
        if user_id and password:
            st.success(f"Welcome back, {user_id}!")
        else:
            st.error("❌ Please enter both ID and password.")
            
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='footer'>Developed by Muzahid | IUBAT Nexus Beta © 2026</div>", unsafe_allow_html=True)
