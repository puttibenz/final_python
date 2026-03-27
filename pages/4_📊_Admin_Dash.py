import streamlit as st
from utils.auth import auth_manager
from database.crud import camp_repo, booking_repo
from components.charts import AdminCharts

# Page Config
st.set_page_config(page_title="Admin Dashboard", page_icon="📊", layout="wide")

auth_manager.check_auth_required()

# Security Check: Ensure only admin can access
user = auth_manager.current_user
if user.get("role") != "admin":
    st.error("⛔ คุณไม่มีสิทธิ์เข้าถึงหน้านี้")
    st.stop()

class AdminDashboard:
    """
    จัดการข้อมูลหลังบ้านสำหรับ Admin
    """
    def __init__(self):
        self.camps = camp_repo.get_all()
        self.bookings = booking_repo.get_all_bookings_detail()

    def render_stats(self):
        """แสดงภาพรวมสถิติ"""
        st.subheader("📈 ภาพรวมระบบ")
        col1, col2, col3 = st.columns(3)
        
        # คำนวณรายได้ (เฉพาะที่ยืนยันแล้วหรือสำเร็จแล้ว)
        total_revenue = sum(b['price'] for b in self.bookings if b.get('status') != 'cancelled')
        
        col1.metric("ทริปทั้งหมด", len(self.camps))
        col2.metric("การจองทั้งหมด", len(self.bookings))
        col3.metric("รายได้ประมาณการ", f"฿{total_revenue:,.0f}")

        st.info(f"💡 รายได้คำนวณจากสถานะ 'ยืนยันแล้ว' และ 'สำเร็จแล้ว' รวมกัน")

    def render_booking_management(self):
        """จัดการสถานะการจอง"""
        st.divider()
        st.subheader("📋 จัดการสถานะการจอง")
        
        if not self.bookings:
            st.info("ยังไม่มีข้อมูลการจอง")
            return

        status_map = {
            "pending_payment": "รอชำระเงิน",
            "confirmed": "ยืนยันแล้ว",
            "completed": "สำเร็จแล้ว",
            "cancelled": "ยกเลิก"
        }

        # แสดงตาราง
        for b in self.bookings:
            with st.expander(f"ID: {b['id']} | {b['username']} - {b['camp_name']} ({status_map.get(b['status'], b['status'])})"):
                c1, c2 = st.columns([2, 1])
                with c1:
                    st.write(f"**ผู้จอง:** {b['username']} ({b['email']})")
                    st.write(f"**ทริป:** {b['camp_name']}")
                    st.write(f"**วันที่จอง:** {b['booked_at'].strftime('%d/%m/%Y %H:%M')}")
                
                with c2:
                    current_status = b['status']
                    options = ["pending_payment", "confirmed", "completed", "cancelled"]
                    new_status = st.selectbox(
                        "เปลี่ยนสถานะ",
                        options,
                        index=options.index(current_status) if current_status in options else 0,
                        key=f"status_{b['id']}",
                        format_func=lambda x: status_map.get(x, x)
                    )
                    
                    if new_status != current_status:
                        if st.button("อัปเดตสถานะ", key=f"btn_{b['id']}"):
                            if booking_repo.update_booking_status(b['id'], new_status):
                                st.success(f"อัปเดตสถานะการจอง #{b['id']} เป็น {status_map[new_status]} สำเร็จ!")
                                st.rerun()
                            else:
                                st.error("ไม่สามารถอัปเดตสถานะได้")

    def render_analytics(self):
        """แสดงกราฟวิเคราะห์ข้อมูล"""
        st.divider()
        st.subheader("📊 การวิเคราะห์ข้อมูล (Analytics)")
        
        if not self.bookings:
            st.info("ยังไม่มีข้อมูลสำหรับการวิเคราะห์")
            return
            
        charts = AdminCharts(self.bookings)
        
        # แถวแรก: สัดส่วนสถานะ และ แคมป์ยอดนิยม
        col1, col2 = st.columns(2)
        with col1:
            charts.render_booking_status_pie()
        with col2:
            charts.render_top_camps_bar()
            
        # แถวที่สอง: แนวโน้มรายได้ และ การจองรายวัน
        col3, col4 = st.columns(2)
        with col3:
            charts.render_revenue_trend()
        with col4:
            charts.render_daily_bookings_area()

    def render(self):
        st.title("📊 แผงควบคุมผู้ดูแลระบบ")
        self.render_stats()
        self.render_analytics()
        self.render_booking_management()

# Instantiate and render
dashboard = AdminDashboard()
dashboard.render()
