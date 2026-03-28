import streamlit as st
from components.camp_card import CampCard
from database.crud import camp_repo, booking_repo
from utils.auth import auth_manager

class ExplorePage:
    """Class สำหรับจัดการหน้า Explore ค้นหาและจองแคมป์"""

    def __init__(self):
        # 1. ตรวจสอบสิทธิ์การเข้าถึง
        auth_manager.check_auth_required()
        self.user_id = st.session_state.user["id"]
        
        # 2. Sync สถานะแคมป์และการจองที่จบลงแล้ว
        camp_repo.sync_ended_camps()
        booking_repo.sync_completed_bookings()
        
        # 3. โหลดข้อมูลเริ่มต้น
        self.camps_data = camp_repo.get_all()
        self.user_booked = booking_repo.get_user_bookings(self.user_id)

    def render_header(self):
        """แสดง CSS และ Header"""
        st.markdown("""
        <style>
            .explore-header { text-align: center; padding: 1.5rem 0 0.5rem; }
            .explore-header h1 {
                font-size: 2.2rem;
                background: linear-gradient(135deg, #2E7D32, #66BB6A);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            .explore-header p { color: #888; font-size: 1rem; }
        </style>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="explore-header">
            <h1>🏕️ ค้นหาทริปแคมป์</h1>
            <p>เลือกทริปที่ใช่แล้วจองเลย!</p>
        </div>
        """, unsafe_allow_html=True)
        st.divider()

    def render_dialogs(self):
        """จัดการ Dialogs ต่างๆ (Booking & Payment)"""
        
        @st.dialog("QR Code ชำระเงิน")
        def payment_dialog(booking_id, camp_name, price):
            st.write(f"**ทริป:** {camp_name}")
            st.write(f"**จำนวนเงิน:** ฿{price:,.0f}")
            qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=PromptPay_Mock_For_{booking_id}"
            st.image(qr_url, caption="สแกนเพื่อชำระเงิน (จำลอง)", width=250)
            if st.button("ชำระเงินเรียบร้อย (Done)", use_container_width=True):
                if booking_repo.complete_payment(booking_id):
                    st.success("🎉 ชำระเงินสำเร็จ! ข้อมูลการจองได้รับการยืนยันแล้ว")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("❌ เกิดข้อผิดพลาด")

        @st.dialog("ยืนยันการจอง")
        def confirm_booking_dialog(camp):
            st.write(f"คุณต้องการจองทริป **{camp['name']}** ใช่หรือไม่?")
            st.write(f"📍 สถานที่: {camp['location']}")
            st.write(f"💰 ราคา: ฿{camp['price']:,.0f}")
            if st.button("ยืนยัน (Yes)", use_container_width=True):
                booking_res = booking_repo.create_booking(self.user_id, camp['id'])
                if isinstance(booking_res, int):
                    st.session_state.pending_booking = {
                        "id": booking_res,
                        "name": camp['name'],
                        "price": camp['price']
                    }
                    st.rerun()
                elif isinstance(booking_res, dict) and "error" in booking_res:
                    st.error(f"❌ จองไม่สำเร็จ: {booking_res['error']}")
                else:
                    st.error("❌ จองไม่สำเร็จ: ไม่สามารถเชื่อมต่อฐานข้อมูลได้")

        # ── เช็คสถานะ Dialog ที่ค้างอยู่ ──
        if "pending_booking" in st.session_state:
            pending = st.session_state.pop("pending_booking")
            payment_dialog(pending["id"], pending["name"], pending["price"])
            
        return confirm_booking_dialog

    def render_filters(self):
        """แสดงส่วนค้นหาและตัวกรอง"""
        with st.container():
            col_search, col_price = st.columns([2, 1])
            with col_search:
                search_query = st.text_input("🔍 ค้นหาชื่อหรือสถานที่", placeholder="เช่น เขาค้อ, กาญจนบุรี")
            with col_price:
                price_range = st.slider("💰 ราคาสูงสุด (฿)", 0, 10000, 10000, step=500)
            
            st.caption(f"📊 ทริปที่มีให้เลือก: {len(self.camps_data)} | จองแล้ว: {len(self.user_booked)}")
        st.divider()
        return search_query, price_range

    def render_grid(self, search_query, price_range, confirm_func):
        """แสดงรายการแคมป์ในรูปแบบ Grid"""
        filtered = [
            c for c in self.camps_data
            if (search_query.lower() in str(c.get("name", "")).lower()
                or search_query.lower() in str(c.get("location", "")).lower())
            and float(c.get("price", 0) or 0) <= price_range
            and c.get("status") == "active"
        ]

        if not filtered:
            if not self.camps_data:
                st.info("🏕️ ยังไม่มีทริปในระบบ — ลองสร้างทริปแรกของคุณ!")
            else:
                st.warning("ไม่พบทริปที่ตรงกับเงื่อนไข ลองปรับตัวกรองดู")
        else:
            cols = st.columns(3)
            for idx, camp in enumerate(filtered):
                with cols[idx % 3]:
                    card = CampCard(camp)
                    is_booked = camp.get("id") in self.user_booked
                    result = card.render(booked=is_booked, user_id=self.user_id)

                    if result:
                        confirm_func(camp)

    def render(self):
        """เมธอดหลักในการแสดงผลหน้าเว็บ"""
        self.render_header()
        confirm_func = self.render_dialogs()
        search_query, price_range = self.render_filters()
        self.render_grid(search_query, price_range, confirm_func)
        
        st.divider()
        st.caption("© 2026 Camping Project Community")

if __name__ == "__main__":
    page = ExplorePage()
    page.render()
