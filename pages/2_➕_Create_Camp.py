import streamlit as st
from components.forms import CampForm
from database.crud import camp_repo
from utils.auth import auth_manager

class CreateCampPage:
    """Class สำหรับจัดการหน้าสร้างทริปแคมป์ใหม่"""

    def __init__(self):
        auth_manager.check_auth_required()
        self.user_id = st.session_state.user["id"]

    def render_header(self):
        """แสดง CSS และ Header"""
        st.markdown("""
        <style>
            .camp-header { text-align: center; padding: 1.5rem 0 0.5rem; }
            .camp-header h1 {
                font-size: 2.2rem;
                background: linear-gradient(135deg, #2E7D32, #66BB6A);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            .camp-header p { color: #888; font-size: 1rem; }
            div[data-testid="stForm"] {
                border: 1px solid #333;
                border-radius: 16px;
                padding: 2rem;
                background-color: #1E1E1E;
            }
        </style>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="camp-header">
            <h1>🏕️ สร้างทริปแคมป์ใหม่</h1>
            <p>กรอกรายละเอียดทริปของคุณ แล้วเผยแพร่ให้คนอื่นเข้าร่วม!</p>
        </div>
        """, unsafe_allow_html=True)
        st.divider()

    def handle_form(self):
        """แสดงฟอร์มและจัดการการบันทึกข้อมูล"""
        form = CampForm()
        result = form.render()

        if result:
            try:
                result["created_by"] = self.user_id
                camp_id = camp_repo.create(result)
                st.balloons()
                st.success(f"🎉 สร้างทริป **{result['name']}** สำเร็จ! (ID: {camp_id})")
            except Exception as e:
                st.error(f"❌ เกิดข้อผิดพลาด: {e}")

    def render_recent_list(self):
        """แสดงรายการทริปที่เคยสร้างไว้แล้วในระบบ"""
        camps = camp_repo.get_all()
        if camps:
            st.divider()
            st.subheader(f"📋 ทริปทั้งหมดในระบบ ({len(camps)} ทริป)")
            for camp in camps:
                price = camp.get("price", 0) or 0
                with st.expander(f"🏕️ {camp['name']} — {camp['location']} | ฿{price:,.0f}/คน"):
                    col1, col2, col3 = st.columns(3)
                    col1.metric("📅 วันเริ่ม", str(camp.get("start_date", "")))
                    col2.metric("⏱️ จำนวนวัน", f"{camp.get('duration', '-')} วัน")
                    col3.metric("👥 รับได้", f"{camp.get('available_slots', camp.get('slots', '-'))} คน")
                    if camp.get("description"):
                        st.write(camp["description"])
                    if camp.get("contact"):
                        st.caption(f"📞 {camp['contact']}")

    def render(self):
        """เมธอดหลักในการแสดงผลหน้าเว็บ"""
        self.render_header()
        self.handle_form()
        self.render_recent_list()

if __name__ == "__main__":
    page = CreateCampPage()
    page.render()
