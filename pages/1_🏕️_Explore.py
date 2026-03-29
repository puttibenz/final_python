import streamlit as st
from components.camp_card import CampCard
from database.crud import camp_repo, booking_repo
from utils.base_page import BasePage

class ExplorePage(BasePage):
    """Class สำหรับจัดการหน้า Explore ค้นหาและจองแคมป์"""

    def __init__(self):
        # เรียก Constructor ของ BasePage (จัดการ Auth และตั้งชื่อหน้า)
        super().__init__(title="⛺ ค้นหาทริปแคมป์", subtitle="เลือกทริปที่ใช่แล้วออกเดินทางไปกับเรา!")
        
        # 1. Sync สถานะแคมป์และการจองที่จบลงแล้ว
        camp_repo.sync_ended_camps()
        booking_repo.sync_completed_bookings()
        
        # 2. โหลดข้อมูลเริ่มต้น
        self.camps_data = camp_repo.get_all()
        self.user_booked = booking_repo.get_user_bookings(self.user_id)

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
        """แสดงรายการแคมป์ในรูปแบบ Grid พร้อม Pagination"""
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
            # ── Pagination Logic ──
            items_per_page = 9
            total_items = len(filtered)
            total_pages = (total_items + items_per_page - 1) // items_per_page
            
            if "current_page" not in st.session_state:
                st.session_state.current_page = 1
            
            # ป้องกันหน้าเกินขอบเขตกรณีเปลี่ยนตัวกรอง
            if st.session_state.current_page > total_pages:
                st.session_state.current_page = 1

            start_idx = (st.session_state.current_page - 1) * items_per_page
            end_idx = start_idx + items_per_page
            page_items = filtered[start_idx:end_idx]

            # ── Render Grid (3 columns) ──
            cols = st.columns(3)
            for idx, camp in enumerate(page_items):
                with cols[idx % 3]:
                    card = CampCard(camp)
                    is_booked = camp.get("id") in self.user_booked
                    result = card.render(booked=is_booked, user_id=self.user_id)

                    if result:
                        confirm_func(camp)

            # ── Pagination Controls ──
            st.write("")
            col_prev, col_page, col_next = st.columns([1, 2, 1])
            with col_prev:
                if st.button("⬅️ ก่อนหน้า", disabled=st.session_state.current_page <= 1, use_container_width=True):
                    st.session_state.current_page -= 1
                    st.rerun()
            with col_page:
                st.markdown(f"<p style='text-align:center;'>หน้า {st.session_state.current_page} จาก {total_pages}</p>", unsafe_allow_html=True)
            with col_next:
                if st.button("ถัดไป ➡️", disabled=st.session_state.current_page >= total_pages, use_container_width=True):
                    st.session_state.current_page += 1
                    st.rerun()

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
