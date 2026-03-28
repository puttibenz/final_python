import streamlit as st
from utils.auth import auth_manager

class LoginPage:
    """Class สำหรับจัดการหน้า Login และ Register (OOP Version)"""

    def __init__(self):
        auth_manager.init_session_state()
        # ── ถ้า Login แล้ว -> Redirect ไป Explore ทันที ──
        if auth_manager.is_logged_in:
            auth_manager.inject_global_css()
            st.switch_page("pages/1_🏕️_Explore.py")

    def render_header(self):
        """แสดง CSS และ Header ของหน้า Login"""
        st.markdown("""
        <style>
            [data-testid="stSidebarNav"] { display: none; }
            section[data-testid="stSidebar"] { display: none; }
            
            .login-header {
                text-align: center;
                margin-bottom: 2rem;
            }
            .login-header h1 {
                color: #66BB6A;
                font-size: 2.2rem;
                margin-bottom: 0.5rem;
            }
        </style>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="login-header">
            <h1>🏕️ Camping Trip</h1>
            <p style="color:#888;">ค้นหาและสร้างทริปแคมป์ที่ใช่สำหรับคุณ</p>
        </div>
        """, unsafe_allow_html=True)

    def render_auth_form(self):
        """แสดงฟอร์ม Login และ Register ในรูปแบบ Card/Tabs"""
        _, col, _ = st.columns([1, 4, 1])

        with col:
            tab1, tab2 = st.tabs(["🔐 เข้าสู่ระบบ", "✨ สมัครสมาชิก"])

            with tab1:
                self._render_login_tab()

            with tab2:
                self._render_register_tab()

    def _render_login_tab(self):
        """Private method สำหรับหน้า Login"""
        with st.form("login_form", clear_on_submit=False):
            st.markdown("### เข้าสู่ระบบ")
            l_email = st.text_input("📧 อีเมล", placeholder="example@email.com")
            l_password = st.text_input("🔑 รหัสผ่าน", type="password")
            st.write("")
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

    def _render_register_tab(self):
        """Private method สำหรับหน้า Register"""
        with st.form("register_form"):
            st.markdown("### สมัครสมาชิก")
            r_username = st.text_input("👤 ชื่อผู้ใช้ (Username)")
            r_email = st.text_input("📧 อีเมล", placeholder="example@email.com")
            
            c1, c2 = st.columns(2)
            with c1:
                r_fullname = st.text_input("📛 ชื่อ-นามสกุล")
            with c2:
                r_phone = st.text_input("📞 เบอร์โทร")
                
            r_password = st.text_input("🔑 รหัสผ่าน", type="password")
            r_confirm = st.text_input("🔄 ยืนยันรหัสผ่าน", type="password")
            
            st.write("")
            r_submit = st.form_submit_button("✨ สร้างบัญชี", use_container_width=True)

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
                            error_msg = msg.get("error") if isinstance(msg, dict) else msg
                            st.error(f"❌ {error_msg}")

    def render(self):
        """เมธอดหลักในการแสดงผลหน้าเว็บ"""
        self.render_header()
        self.render_auth_form()
        st.markdown("---")
        st.caption("<p style='text-align:center;'>© 2026 Camping Project Community</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    page = LoginPage()
    page.render()
