import streamlit as st
from utils.auth import auth_manager

st.set_page_config(page_title="Camping Trip 🏕️", page_icon="🏕️", layout="centered")
auth_manager.init_session_state()

# ── ซ่อน sidebar navigation ถ้ายังไม่ login ──
if not st.session_state.get("is_logged_in"):
    st.markdown("""
    <style>
        [data-testid="stSidebarNav"] { display: none; }
        section[data-testid="stSidebar"] { display: none; }
    </style>
    """, unsafe_allow_html=True)

    # ── Header ──
    st.markdown("""
    <div style="text-align:center; padding: 2rem 0 1rem;">
        <h1 style="font-size:2.5rem;">🏕️ Camping Trip</h1>
        <p style="color:#888; font-size:1.1rem;">ค้นหาและสร้างทริปแคมป์ที่ใช่สำหรับคุณ</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # ── จัดกลางฟอร์ม ──
    _, col, _ = st.columns([1, 2, 1])
    with col:
        tab1, tab2 = st.tabs(["🔑 เข้าสู่ระบบ", "✨ สมัครสมาชิก"])

        with tab1:
            with st.form("login_form"):
                l_email = st.text_input("อีเมล", placeholder="you@email.com")
                l_password = st.text_input("รหัสผ่าน", type="password")
                l_submit = st.form_submit_button("🚀 เข้าสู่ระบบ", use_container_width=True)

                if l_submit:
                    if not l_email or not l_password:
                        st.warning("⚠️ กรุณากรอกข้อมูลให้ครบ")
                    else:
                        with st.spinner("กำลังตรวจสอบ..."):
                            success, msg = auth_manager.login(l_email, l_password)
                            if success:
                                st.success(msg)
                                st.rerun()
                            else:
                                st.error(f"❌ {msg}")

        with tab2:
            with st.form("register_form"):
                r_username = st.text_input("ชื่อผู้ใช้ (Username)")
                r_fullname = st.text_input("ชื่อ-นามสกุล (ไม่บังคับ)")
                r_email = st.text_input("อีเมล", placeholder="you@email.com")
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
                            success, msg = auth_manager.register(r_username, r_email, r_password, r_fullname or None, r_phone or None)
                            if success:
                                st.success(f"✅ {msg}")
                            else:
                                st.error(f"❌ {msg}")

    st.stop()  # ⛔ หยุดตรงนี้ — ไม่ให้ไปต่อ

# ══════════════════════════════════════════
# ถ้า login แล้ว → แสดง sidebar + ต้อนรับ
# ══════════════════════════════════════════
user = st.session_state.user

with st.sidebar:
    st.markdown(f"### 👤 {user.get('username', 'User')}")
    st.caption(f"📧 {user.get('email', '')}")
    st.caption(f"🏷️ สิทธิ์: {user.get('role', 'user')}")
    st.divider()
    if st.button("🚪 ออกจากระบบ", use_container_width=True):
        auth_manager.logout()

st.markdown("""
<div style="text-align:center; padding: 2rem 0;">
    <h1>🏕️ ยินดีต้อนรับ!</h1>
    <p style="color:#888; font-size:1.1rem;">เลือกเมนูจาก sidebar เพื่อเริ่มต้นใช้งาน</p>
</div>
""", unsafe_allow_html=True)
