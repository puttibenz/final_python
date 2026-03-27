import streamlit as st
from datetime import date, timedelta


class CampForm:
    """Component สำหรับฟอร์มสร้างทริปแคมป์"""

    def __init__(self):
        self.data = {}

    def render(self):
        with st.form("create_camp_form", clear_on_submit=True):

            # ─ ข้อมูลทั่วไป ─
            st.markdown('<p style="font-size:0.85rem;font-weight:600;color:#66BB6A;text-transform:uppercase;letter-spacing:1px;margin-bottom:0.3rem;">📋 ข้อมูลทั่วไป</p>', unsafe_allow_html=True)

            name = st.text_input("ชื่อทริป *", placeholder="เช่น แคมป์ดอยอินทนนท์ ชมทะเลหมอก",
                                 help="ตั้งชื่อทริปให้น่าสนใจ ดึงดูดคนเข้าร่วม")

            col1, col2 = st.columns(2)
            with col1:
                location = st.text_input("สถานที่ / จังหวัด *", placeholder="เช่น เชียงใหม่",
                                         help="ระบุจังหวัดหรือสถานที่จัดแคมป์")
            with col2:
                start_date = st.date_input("วันเริ่มทริป *", min_value=date.today(), value=date.today() + timedelta(days=7),
                                           help="เลือกวันที่เริ่มต้นทริป")

            col3, col4 = st.columns(2)
            with col3:
                duration = st.number_input("จำนวนวัน", min_value=1, max_value=30, value=2,
                                           help="ทริปนี้กี่วัน?")
            with col4:
                price = st.number_input("ราคา (บาท/คน) *", min_value=0, max_value=100000, value=1500, step=100,
                                        help="ราคาต่อคน รวมค่าใช้จ่ายทั้งหมด")

            # ─ ที่นั่ง ─
            st.markdown('<p style="font-size:0.85rem;font-weight:600;color:#66BB6A;text-transform:uppercase;letter-spacing:1px;margin-top:1.5rem;margin-bottom:0.3rem;">🎟️ จำนวนที่นั่ง</p>', unsafe_allow_html=True)

            slots = st.slider("จำนวนคนที่รับได้", min_value=1, max_value=100, value=20,
                              help="เลือกจำนวนสมาชิกสูงสุดที่รับได้")
            st.caption(f"รับสมาชิกได้สูงสุด **{slots}** คน")

            # ─ รายละเอียด ─
            st.markdown('<p style="font-size:0.85rem;font-weight:600;color:#66BB6A;text-transform:uppercase;letter-spacing:1px;margin-top:1.5rem;margin-bottom:0.3rem;">📝 รายละเอียด</p>', unsafe_allow_html=True)

            description = st.text_area(
                "รายละเอียดทริป",
                height=150,
                placeholder="บรรยายความพิเศษของทริปนี้ เช่น กิจกรรม, สิ่งที่รวม, ข้อควรเตรียม...",
                help="อธิบายกิจกรรม สิ่งที่รวมในราคา ข้อควรเตรียมตัว"
            )

            image_url = st.text_input("URL รูปภาพปก (ไม่บังคับ)", placeholder="https://example.com/camp-photo.jpg",
                                      help="ใส่ลิงก์รูปภาพเพื่อเป็นหน้าปกทริป")

            # ─ ช่องทางติดต่อ ─
            st.markdown('<p style="font-size:0.85rem;font-weight:600;color:#66BB6A;text-transform:uppercase;letter-spacing:1px;margin-top:1.5rem;margin-bottom:0.3rem;">📞 ช่องทางติดต่อ</p>', unsafe_allow_html=True)

            col5, col6 = st.columns(2)
            with col5:
                contact = st.text_input("เบอร์โทร / Line", placeholder="08x-xxx-xxxx",
                                        help="เบอร์โทรหรือ Line ID สำหรับติดต่อ")
            with col6:
                facebook_link = st.text_input("Facebook Link (ไม่บังคับ)", placeholder="https://facebook.com/...",
                                              help="ลิงก์หน้า Facebook หรือโพสต์ของทริป")

            st.divider()

            submitted = st.form_submit_button("🚀 เผยแพร่ทริป", use_container_width=True, type="primary")

            if submitted:
                if not name or not location or not price:
                    st.error("❌ กรุณากรอกข้อมูลที่มีเครื่องหมาย * ให้ครบ")
                    return None

                self.data = {
                    "name": name,
                    "location": location,
                    "start_date": str(start_date),
                    "duration": duration,
                    "price": price,
                    "slots": slots,
                    "available_slots": slots,
                    "description": description or None,
                    "image_url": image_url or None,
                    "contact": contact or None,
                    "facebook_link": facebook_link or None,
                    "status": "active",
                }
                return self.data

        return None
