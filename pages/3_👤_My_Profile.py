import streamlit as st
from utils.auth import init_session_state, check_auth_required

st.set_page_config(page_title="My Profile", page_icon="👤", layout="centered")
init_session_state()
check_auth_required()

user = st.session_state.user
st.title("👤 โปรไฟล์ของฉัน")
st.info(f"ชื่อผู้ใช้: {user.get('username', '')} | อีเมล: {user.get('email', '')}")
st.warning("🚧 หน้านี้กำลังพัฒนา")