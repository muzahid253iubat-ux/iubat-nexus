import streamlit as st

# Language footer implementation with custom spacing
footer_html = """
<style>
.language-footer {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 15px;
    font-size: 13px;
    color: #8a8d91;
    margin-top: 80px; /* Adjust this value to move it further down */
    padding-bottom: 20px;
}
.language-footer a {
    color: #8a8d91;
    text-decoration: none;
}
.language-footer a:hover {
    text-decoration: underline;
}
</style>

<div class="language-footer">
    <a href="#">English (UK)</a>
    <a href="#">বাংলা</a>
    <a href="#">অসমীয়া</a>
    <a href="#">हिन्दी</a>
    <a href="#">नेपाली</a>
    <a href="#">Bahasa Indonesia</a>
    <a href="#">العربية</a>
    <a href="#">More languages...</a>
</div>
"""

st.markdown(footer_html, unsafe_allow_html=True)
