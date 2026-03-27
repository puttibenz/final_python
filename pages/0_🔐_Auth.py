import streamlit as st
from utils.auth import init_session_state, logout

st.set_page_config(page_title="Auth - Camping Project", page_icon="🔐", layout="centered")
init_session_state()

# ถ้ายังไม่ login → redirect ไป main.py
if not st.session_state.get("is_logged_in"):
    st.warning("กรุณาเข้าสู่ระบบที่หน้าแรก")
    st.switch_page("main.py")

# ถ้า login แล้ว → แสดงข้อมูล + ปุ่ม logout
user = st.session_state.user
st.title("🔐 บัญชีของฉัน")
st.success(f"✅ ยินดีต้อนรับ **{user.get('username', 'User')}**!")
st.info(f"สิทธิ์: {user.get('role', 'user')}")
if st.button("🚪 ออกจากระบบ", use_container_width=True):
    logout()
