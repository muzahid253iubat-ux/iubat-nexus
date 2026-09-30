import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="IUBAT Nexus | Smart Portal",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling, shifting elements down, and adding the footer language bar
st.markdown("""
    <style>
    /* Main container spacing to push login box down */
    .block-container {
        padding-top: 4rem;
        padding-bottom: 5rem;
    }
    
    /* Login Box Styling */
    .login-container {
        margin-top: 50px;
    }

    /* Footer Language Bar Styling (Facebook Style) */
    .footer-languages {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: rgba(24, 25, 26, 0.9);
        color: #b0b3b8;
        padding: 12px 20px;
        text-align: center;
        font-size: 13px;
        z-index: 999;
        border-top: 1px solid #38393b;
    }
    
    .footer-languages span {
        margin: 0 10px;
        cursor: pointer;
        display: inline-block;
    }
    
    .footer-languages span:hover {
        text-decoration: underline;
        color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

# Layout Columns
col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown("## **All of IUBAT, Working For You.**")
    st.markdown("Sign in with your student ID and password to access smart shuttle schedules, live GPS tracking, faculty directories, and campus updates instantly.")

with col2:
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown("### **Log in**")
    
    student_id = st.text_input("ID Number", placeholder="Student ID Number")
    password = st.text_input("Password", type="password", placeholder="Password")
    remember_session = st.checkbox("Remember session")
    
    if st.button("Log in", type="primary"):
        if student_id and password:
            st.success("Login successful!")
        else:
            st.warning("Please enter your ID and password.")
            
    st.markdown("[Forgotten password?](#)")
    st.markdown("---")
    st.markdown("[Create new account](#)")
    st.markdown('</div>', unsafe_allow_html=True)

# Facebook-style Footer Languages Bar
st.markdown("""
    <div class="footer-languages">
        <span>English (UK)</span>
        <span>বাংলা</span>
        <span>অসমীয়া</span>
        <span>हिन्दी</span>
        <span>नेपाली</span>
        <span>Bahasa Indonesia</span>
        <span>العربية</span>
        <span>More languages...</span>
    </div>
""", unsafe_allow_html=True)
