import streamlit as st
from utils.auth import init_session_state, login, register, logout

st.set_page_config(page_title="Auth - Camping Project", page_icon="🔐", layout="centered")

init_session_state()

st.title("🔐 เข้าสู่ระบบ / สมัครสมาชิก")

if st.session_state.is_logged_in:
    user = st.session_state.user
    st.success(f"✅ ยินดีต้อนรับ **{user.get('username', 'User')}**!")
    st.info(f"สิทธิ์: {user.get('role', 'user')}")
    if st.button("🚪 ออกจากระบบ", use_container_width=True):
        logout()
else:
    tab1, tab2 = st.tabs(["เข้าสู่ระบบ", "สมัครสมาชิก"])

    with tab1:
        st.header("เข้าสู่ระบบ")
        with st.form("login_form"):
            l_email = st.text_input("อีเมล")
            l_password = st.text_input("รหัสผ่าน", type="password")
            l_submit = st.form_submit_button("🚀 เข้าสู่ระบบ", use_container_width=True)

            if l_submit:
                if not l_email or not l_password:
                    st.warning("⚠️ กรุณากรอกข้อมูลให้ครบ")
                else:
                    with st.spinner("กำลังตรวจสอบ..."):
                        success, msg = login(l_email, l_password)
                        if success:
                            st.success(msg)
                            st.rerun()
                        else:
                            st.error(f"❌ {msg}")

    with tab2:
        st.header("สร้างบัญชีใหม่")
        with st.form("register_form"):
            r_username = st.text_input("ชื่อผู้ใช้ (Username)")
            r_fullname = st.text_input("ชื่อ-นามสกุล (ไม่บังคับ)")
            r_email = st.text_input("อีเมล")
            r_phone = st.text_input("เบอร์โทร (ไม่บังคับ)")
            r_password = st.text_input("รหัสผ่าน", type="password")
            r_confirm = st.text_input("ยืนยันรหัสผ่าน", type="password")
            r_submit = st.form_submit_button("✨ สมัครสมาชิก", use_container_width=True)

            if r_submit:
                if not r_username or not r_email or not r_password:
                    st.warning("⚠️ กรุณากรอกข้อมูลให้ครบ")
                elif r_password != r_confirm:
                    st.error("❌ รหัสผ่านไม่ตรงกัน")
                elif len(r_password) < 6:
                    st.warning("⚠️ รหัสผ่านต้องมีอย่างน้อย 6 ตัวอักษร")
                else:
                    with st.spinner("กำลังสมัครสมาชิก..."):
                        success, msg = register(r_username, r_email, r_password, r_fullname or None, r_phone or None)
                        if success:
                            st.success(f"✅ {msg}")
                        else:
                            st.error(f"❌ {msg}")
