import streamlit as st
from utils.auth import init_session_state, check_auth_required

st.set_page_config(page_title="Admin Dashboard", page_icon="📊", layout="wide")
init_session_state()
check_auth_required()

user = st.session_state.user
if user.get("role") != "admin":
    st.error("⛔ คุณไม่มีสิทธิ์เข้าถึงหน้านี้")
    st.stop()

st.title("📊 Admin Dashboard")
st.warning("🚧 หน้านี้กำลังพัฒนา")