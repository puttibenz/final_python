import streamlit as st

# Configure the page
st.set_page_config(
    page_title="Camp Booking System",
    page_icon="🏕️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import auth utilities
from utils.auth import init_session_state

# Initialize session state
init_session_state()

# Sidebar navigation
st.sidebar.title("🏕️ Camp Booking")
st.sidebar.markdown("---")

# Navigation menu
pages = {
    "🔐 เข้าสู่ระบบ": "0_🔐_Auth.py",
    "🏕️ สำรวจแคมป์": "1_🏕️_Explore.py",
    "➕ สร้างแคมป์": "2_➕_Create_Camp.py",
    "👤 โปรไฟล์ของฉัน": "3_👤_My_Profile.py",
    "📊 แดชบอร์ดผู้ดูแล": "4_📊_Admin_Dash.py"
}

# Show user status in sidebar
if st.session_state.get("is_logged_in", False):
    st.sidebar.success(f"Registered: {st.session_state.username}")
    if st.sidebar.button("🚪 Logout"):
        from utils.auth import logout
        logout()
else:
    st.sidebar.info("Please log in")

st.sidebar.markdown("---")

# Page selection
selected_page = st.sidebar.radio("เมนู", list(pages.keys()))

# Load the selected page
page_file = pages[selected_page]
with open(f"pages/{page_file}", 'r', encoding='utf-8') as f:
    exec(f.read())