import streamlit as st
import bcrypt
from database.crud import user_repo

class AuthManager:
    """Class สำหรับจัดการ Authentication และ User Session (OOP Version)"""

    def __init__(self):
        """Initialize session state อัตโนมัติเมื่อมีการสร้าง instance"""
        self.init_session_state()

    def init_session_state(self):
        """ตั้งค่าเริ่มต้นให้กับ st.session_state"""
        if "is_logged_in" not in st.session_state:
            st.session_state.is_logged_in = False
        if "user" not in st.session_state:
            st.session_state.user = None

    def _hash_password(self, password: str) -> str:
        """เข้ารหัสผ่าน (Private Method)"""
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def _verify_password(self, password: str, hashed: str) -> bool:
        """ตรวจสอบความถูกต้องของรหัสผ่าน (Private Method)"""
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))

    def login(self, email: str, password: str) -> tuple[bool, str]:
        """ตรวจสอบข้อมูลการล็อกอินและบันทึกลง Session"""
        try:
            user = user_repo.get_user_by_email(email)
            if not user:
                return False, "ไม่พบอีเมลนี้ในระบบ"
            
            if not self._verify_password(password, user["password_hash"]):
                return False, "รหัสผ่านไม่ถูกต้อง"
            
            # บันทึกสถานะการล็อกอินลงใน Streamlit Session
            st.session_state.is_logged_in = True
            st.session_state.user = {
                "id": user["id"],
                "username": user["username"],
                "email": user["email"],
                "full_name": user.get("full_name"),
                "role": user.get("role", "user"),
                "phone": user.get("phone"),
            }
            return True, "เข้าสู่ระบบสำเร็จ!"
        except Exception as e:
            return False, f"เกิดข้อผิดพลาด: {str(e)}"

    def register(self, username: str, email: str, password: str, full_name: str = None, phone: str = None) -> tuple[bool, str]:
        """ลงทะเบียนผู้ใช้ใหม่"""
        try:
            existing = user_repo.get_user_by_email(email)
            if existing:
                return False, "อีเมลนี้ถูกใช้งานแล้ว"
            
            hashed_pw = self._hash_password(password)
            user_id = user_repo.create_user(username, email, hashed_pw, full_name, phone)
            
            if user_id:
                return True, "สมัครสมาชิกสำเร็จ! กรุณาเข้าสู่ระบบ"
            return False, "เกิดข้อผิดพลาดในการบันทึกข้อมูล กรุณาลองใหม่"
        except Exception as e:
            return False, f"เกิดข้อผิดพลาด: {str(e)}"

    def logout(self):
        """ออกจากระบบและล้าง Session"""
        st.session_state.is_logged_in = False
        st.session_state.user = None
        st.rerun()

    def render_sidebar_info(self):
        """แสดงข้อมูลผู้ใช้และปุ่ม Logout ใน Sidebar (ถาวรทุกหน้า)"""
        if self.is_logged_in:
            user = self.current_user
            with st.sidebar:
                st.markdown(f"### 👤 {user.get('username', 'User')}")
                st.caption(f"📧 {user.get('email', '')}")
                st.caption(f"🏷️ สิทธิ์: {user.get('role', 'user')}")
                
                # แสดง Balance แบบสวยๆ
                from database.crud import user_repo
                latest_user = user_repo.get_user_by_id(user["id"])
                balance = latest_user.get("balance", 0) if latest_user else 0
                st.markdown(f"**💰 ยอดเงิน: ฿{balance:,.2f}**")
                
                st.divider()
                if st.button("🚪 ออกจากระบบ", key="sidebar_logout", use_container_width=True):
                    self.logout()

    def inject_global_css(self):
        """ใส่ CSS เพื่อซ่อนเมนูที่ไม่จำเป็นเมื่อ Login แล้ว"""
        if self.is_logged_in:
            user = self.current_user
            
            # CSS พื้นฐาน: ซ่อนหน้า Main (index 1)
            hide_css = """
            <style>
                /* ซ่อนหน้า Main (index 1) ใน Sidebar Nav */
                [data-testid="stSidebarNav"] li:nth-child(1) {
                    display: none;
                }
            """
            
            # ถ้าไม่ใช่ admin ให้ซ่อนหน้า Admin Dash (ปกติจะเป็นหน้าสุดท้าย)
            if user.get("role") != "admin":
                hide_css += """
                /* ซ่อนหน้า Admin Dash สำหรับผู้ใช้ทั่วไป */
                [data-testid="stSidebarNav"] li:nth-child(5) {
                    display: none;
                }
                """
                
            hide_css += "</style>"
            st.markdown(hide_css, unsafe_allow_html=True)

    def check_auth_required(self, redirect_page: str = "main.py"):
        """Middleware ตรวจสอบว่าต้องล็อกอินก่อนถึงจะเข้าถึงหน้านี้ได้"""
        if not st.session_state.get("is_logged_in", False):
            st.warning("กรุณาเข้าสู่ระบบก่อนใช้งาน")
            st.switch_page(redirect_page)
        else:
            self.inject_global_css()
            self.render_sidebar_info()

    @property
    def current_user(self):
        """Helper ดึงข้อมูลผู้ใช้ปัจจุบัน"""
        return st.session_state.get("user")

    @property
    def is_logged_in(self) -> bool:
        """Helper เช็คว่าล็อกอินอยู่หรือไม่"""
        return st.session_state.get("is_logged_in", False)


# สร้าง Global Instance เพื่อความสะดวกในการใช้งานข้ามไฟล์
auth_manager = AuthManager()

# Bridge Functions เพื่อรองรับ Code เก่า (หากต้องการเปลี่ยนทีเดียวให้ข้ามส่วนนี้)
def init_session_state():
    auth_manager.init_session_state()

def login(email, password):
    return auth_manager.login(email, password)

def register(username, email, password, full_name=None, phone=None):
    return auth_manager.register(username, email, password, full_name, phone)

def logout():
    auth_manager.logout()

def check_auth_required():
    auth_manager.check_auth_required()
