import streamlit as st
from database import setup_database
from utils.auth import register_new_user, login_user

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Authentication", page_icon="🔐")

# ==========================================
# ⚡ ใช้ Cache เพื่อเชื่อมต่อฐานข้อมูลแค่ครั้งเดียว (แก้เว็บอืด/โหลดซ้ำ)
# ==========================================
@st.cache_resource
def get_db():
    return setup_database()

try:
    db = get_db()
except Exception as e:
    st.error(f"ไม่สามารถเชื่อมต่อฐานข้อมูลได้: {e}")
    st.stop()

st.title("🔐 เข้าสู่ระบบ / สมัครสมาชิก")

# ==========================================
# 🟢 เช็กสถานะ: ถ้าล็อกอินอยู่แล้ว ให้แสดงข้อมูล Profile
# ==========================================
if st.session_state.get("logged_in"):
    st.success(f"✅ ยินดีต้อนรับคุณ **{st.session_state['user']['Name']}**")
    st.info(f"สิทธิ์การใช้งาน: {st.session_state['user']['Role']}")
    
    if st.button("🚪 ออกจากระบบ (Logout)"):
        st.session_state.clear()
        st.rerun()
    st.stop() # หยุดการทำงานตรงนี้ ไม่แสดงฟอร์มด้านล่าง

# ==========================================
# 🔵 ถ้ายังไม่ล็อกอิน: แสดงแท็บ Login และ Register
# ==========================================
tab_login, tab_register = st.tabs(["เข้าสู่ระบบ (Login)", "สมัครสมาชิก (Register)"])

# --- Tab 1: เข้าสู่ระบบ ---
with tab_login:
    st.header("เข้าสู่ระบบ")
    with st.form("login_form"):
        login_email = st.text_input("อีเมล")
        login_password = st.text_input("รหัสผ่าน", type="password")
        btn_login = st.form_submit_button("เข้าสู่ระบบ")

    if btn_login:
        if not login_email or not login_password:
            st.warning("⚠️ กรุณากรอกข้อมูลให้ครบถ้วน")
        else:
            with st.spinner("กำลังตรวจสอบข้อมูล..."):
                is_success, result = login_user(db, login_email, login_password)
                
                if is_success:
                    st.session_state["logged_in"] = True
                    st.session_state["user"] = result
                    st.success("เข้าสู่ระบบสำเร็จ! กำลังพาดาวน์โหลดหน้าใหม่...")
                    st.rerun()
                else:
                    st.error(f"❌ {result}")

# --- Tab 2: สมัครสมาชิก ---
with tab_register:
    st.header("สร้างบัญชีใหม่")
    with st.form("register_form"):
        reg_name = st.text_input("ชื่อ-นามสกุล")
        reg_email = st.text_input("อีเมล")
        reg_password = st.text_input("รหัสผ่าน", type="password")
        reg_confirm = st.text_input("ยืนยันรหัสผ่าน", type="password")
        btn_register = st.form_submit_button("สมัครสมาชิก")

    if btn_register:
        if not reg_name or not reg_email or not reg_password:
            st.warning("⚠️ กรุณากรอกข้อมูลให้ครบถ้วน")
        elif reg_password != reg_confirm:
            st.error("❌ รหัสผ่านและการยืนยันรหัสผ่านไม่ตรงกัน")
        elif len(reg_password) < 6:
            st.warning("⚠️ รหัสผ่านต้องมีความยาวอย่างน้อย 6 ตัวอักษร")
        else:
            with st.spinner("กำลังลงทะเบียน..."):
                is_success, message = register_new_user(db, reg_name, reg_email, reg_password)
                if is_success:
                    st.success(f"✅ {message}")
                    st.info("กรุณาสลับไปที่แท็บ 'เข้าสู่ระบบ (Login)' เพื่อเริ่มต้นใช้งาน")
                else:
                    st.error(f"❌ {message}")