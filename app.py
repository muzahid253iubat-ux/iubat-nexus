import streamlit as st

# Page configuration for mobile-first layout
st.set_page_config(
    page_title="IUBAT Nexus",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for clean mobile look
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .main {
        background-color: #0e1117;
    }
    .stButton>button {
        width: 100%;
        background-color: #1b263b;
        color: white;
        border-radius: 12px;
        height: 48px;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        background-color: #415a77;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Main Login UI Container
with st.container():
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: white; font-size: 28px;'>IUBAT Nexus</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #adb5bd; font-size: 14px;'>Excellence in Higher Education and Research</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    student_id = st.text_input("ID Number *", placeholder="e.g. 2530xxxx")
    password = st.text_input("Password *", type="password", placeholder="••••••••")
    remember_me = st.checkbox("Remember me")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("Submit"):
        if student_id and password:
            st.success(f"Welcome back, {student_id}!")
        else:
            st.error("Please enter both ID Number and Password.")
            
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #6c757d; font-size: 12px;'>Version : 1.0.0 Beta<br>© 2026 IUBAT Nexus</p>", unsafe_allow_html=True)
