import streamlit as st
from datetime import datetime
import sys
import os

# Add the parent directory to the path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.auth import check_auth_required, init_session_state
from database.crud import get_user_by_username, get_user_bookings, get_user_stats

# Initialize session state
init_session_state()

# Check if user is logged in
check_auth_required()

# Page configuration
st.set_page_config(
    page_title="My Profile - Camp Booking",
    page_icon="👤",
    layout="wide"
)

# Title
st.title("👤 โปรไฟล์ของฉัน - My Profile")
st.markdown("---")

# Get current user
username = st.session_state.username
user = get_user_by_username(username)

if not user:
    st.error("ไม่พบข้อมูลผู้ใช้")
    st.stop()

# User Information Section
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("ข้อมูลส่วนตัว")
    st.write(f"**ชื่อผู้ใช้:** {user.username}")
    st.write(f"**ชื่อเต็ม:** {user.full_name}")
    st.write(f"**อีเมล:** {user.email}")
    if user.phone:
        st.write(f"**โทรศัพท์:** {user.phone}")
    st.write(f"**วันที่สมัคร:** {user.created_at.strftime('%d/%m/%Y')}")

with col2:
    # Quick Stats
    st.subheader("สถิติการใช้งาน")
    stats = get_user_stats(user.id)

    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

    with stat_col1:
        st.metric("การจองทั้งหมด", stats["total_bookings"])

    with stat_col2:
        st.metric("การจองที่สำเร็จ", stats["completed_bookings"])

    with stat_col3:
        st.metric("การจองที่ยกเลิก", stats["cancelled_bookings"])

    with stat_col4:
        st.metric("ยอดใช้จ่ายรวม", f"฿{stats['total_spent']:,.0f}")

    # Additional stats
    st.markdown("---")
    st.write(f"**ค่าเฉลี่ยต่อการจอง:** ฿{stats['average_booking_value']:,.0f}")
    st.write(f"**สถานที่โปรด:** {stats['favorite_location']}")

# Booking History Section
st.markdown("---")
st.subheader("📋 ประวัติการจอง")

bookings = get_user_bookings(user.id)

if not bookings:
    st.info("ยังไม่มีประวัติการจอง")
else:
    # Filter options with control
    col_control, col_filter1, col_filter2 = st.columns([1, 1, 1])

    with col_control:
        # ควบคุมการแสดงผล selectbox
        if "filter_disabled" not in st.session_state:
            st.session_state.filter_disabled = True  # ปิดใช้งานโดย default

        st.checkbox("เปิดใช้งานตัวกรอง", key="filter_disabled", value=False)

        visibility_options = ["visible", "hidden", "collapsed"]
        if "filter_visibility" not in st.session_state:
            st.session_state.filter_visibility = "visible"

        st.radio(
            "การแสดงป้ายชื่อ",
            key="filter_visibility",
            options=visibility_options,
            format_func=lambda x: {
                "visible": "แสดง",
                "hidden": "ซ่อน",
                "collapsed": "ยุบ"
            }.get(x, x),
            index=0
        )

    with col_filter1:
        status_filter = st.selectbox(
            "กรองตามสถานะ",
            ["ทั้งหมด", "confirmed", "completed", "cancelled"],
            format_func=lambda x: {
                "ทั้งหมด": "ทั้งหมด",
                "confirmed": "ยืนยันแล้ว",
                "completed": "เสร็จสิ้น",
                "cancelled": "ยกเลิก"
            }.get(x, x),
            label_visibility=st.session_state.filter_visibility,
            disabled=not st.session_state.filter_disabled,
            key="status_filter"
        )

    with col_filter2:
        sort_by = st.selectbox(
            "เรียงตาม",
            ["created_at", "check_in_date", "total_price"],
            format_func=lambda x: {
                "created_at": "วันที่จอง",
                "check_in_date": "วันที่เช็คอิน",
                "total_price": "ราคา"
            }.get(x, x),
            label_visibility=st.session_state.filter_visibility,
            disabled=not st.session_state.filter_disabled,
            key="sort_filter"
        )

    # Filter bookings
    if status_filter != "ทั้งหมด":
        filtered_bookings = [b for b in bookings if b.status == status_filter]
    else:
        filtered_bookings = bookings

    # Sort bookings
    if sort_by == "created_at":
        filtered_bookings.sort(key=lambda x: x.created_at, reverse=True)
    elif sort_by == "check_in_date":
        filtered_bookings.sort(key=lambda x: x.check_in_date, reverse=True)
    elif sort_by == "total_price":
        filtered_bookings.sort(key=lambda x: x.total_price, reverse=True)

    # Display bookings
    for booking in filtered_bookings:
        with st.container():
            # Status color coding
            status_colors = {
                "confirmed": "🟡",
                "completed": "🟢",
                "cancelled": "🔴"
            }
            status_text = {
                "confirmed": "ยืนยันแล้ว",
                "completed": "เสร็จสิ้น",
                "cancelled": "ยกเลิก"
            }

            col1, col2, col3 = st.columns([2, 2, 1])

            with col1:
                st.write(f"**{booking.camp_name}**")
                st.write(f"📍 {booking.location}")
                st.write(f"👥 {booking.guests} คน")

            with col2:
                st.write(f"📅 เช็คอิน: {booking.check_in_date.strftime('%d/%m/%Y')}")
                st.write(f"📅 เช็คเอาท์: {booking.check_out_date.strftime('%d/%m/%Y')}")
                st.write(f"📝 จองเมื่อ: {booking.created_at.strftime('%d/%m/%Y')}")

            with col3:
                st.write(f"{status_colors.get(booking.status, '⚪')} {status_text.get(booking.status, booking.status)}")
                st.write(f"💰 ฿{booking.total_price:,.0f}")

            st.markdown("---")

# Logout button
st.markdown("---")
if st.button("🚪 ออกจากระบบ", type="secondary"):
    from utils.auth import logout
    logout()