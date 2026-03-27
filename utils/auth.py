import streamlit as st
import bcrypt
from database.crud import user_repo


def init_session_state():
    """Initialize session state for auth."""
    if "is_logged_in" not in st.session_state:
        st.session_state.is_logged_in = False
    if "user" not in st.session_state:
        st.session_state.user = None


def _hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def _verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))


def login(email, password):
    """Login ด้วย email + password ตรวจกับ MySQL."""
    try:
        user = user_repo.get_user_by_email(email)
        if not user:
            return False, "ไม่พบอีเมลนี้ในระบบ"
        if not _verify_password(password, user["password_hash"]):
            return False, "รหัสผ่านไม่ถูกต้อง"
        st.session_state.is_logged_in = True
        st.session_state.user = {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "full_name": user["full_name"],
            "role": user["role"],
            "phone": user["phone"],
        }
        return True, "เข้าสู่ระบบสำเร็จ!"
    except Exception as e:
        return False, str(e)


def register(username, email, password, full_name=None, phone=None):
    """สมัครสมาชิก — hash password แล้วเก็บลง MySQL."""
    try:
        existing = user_repo.get_user_by_email(email)
        if existing:
            return False, "อีเมลนี้ถูกใช้งานแล้ว"
        hashed = _hash_password(password)
        user_id = user_repo.create_user(username, email, hashed, full_name, phone)
        if user_id:
            return True, "สมัครสมาชิกสำเร็จ! กรุณาเข้าสู่ระบบ"
        return False, "เกิดข้อผิดพลาด กรุณาลองใหม่"
    except Exception as e:
        return False, str(e)


def logout():
    """Clear session."""
    st.session_state.is_logged_in = False
    st.session_state.user = None
    st.rerun()


def check_auth_required():
    """Call this on pages that require a login."""
    if not st.session_state.get("is_logged_in", False):
        st.warning("กรุณาเข้าสู่ระบบก่อนใช้งานหน้านี้")
        st.stop()
