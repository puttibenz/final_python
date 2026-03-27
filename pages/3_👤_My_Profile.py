import streamlit as st
from utils.auth import auth_manager
from database.crud import user_repo, booking_repo

st.set_page_config(page_title="My Profile", page_icon="👤", layout="wide")
auth_manager.check_auth_required()

user = auth_manager.current_user
user_id = user["id"]

# ── Header ──
st.title("👤 โปรไฟล์ของฉัน")
st.markdown("---")

# ── ข้อมูลส่วนตัว + สถิติ ──
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("ข้อมูลส่วนตัว")
    st.write(f"**ชื่อผู้ใช้:** {user.get('username', '-')}")
    st.write(f"**ชื่อเต็ม:** {user.get('full_name', '-') or '-'}")
    st.write(f"**อีเมล:** {user.get('email', '-')}")
    if user.get("phone"):
        st.write(f"**โทรศัพท์:** {user['phone']}")
    st.write(f"**สิทธิ์:** {user.get('role', 'user')}")
    
    # ดึงข้อมูลผู้ใช้ล่าสุดเพื่อดู balance (st.session_state อาจยังไม่อัปเดต)
    latest_user = user_repo.get_user_by_id(user_id)
    balance = latest_user.get("balance", 0) if latest_user else 0
    st.markdown(f"### 💰 ยอดเงินในบัญชี: <span style='color:#66BB6A;'>฿{balance:,.2f}</span>", unsafe_allow_html=True)
    
    if user.get("created_at"):
        st.write(f"**วันที่สมัคร:** {user['created_at'].strftime('%d/%m/%Y')}")

with col2:
    st.subheader("สถิติการใช้งาน")
    stats = booking_repo.get_user_stats(user_id)

    if stats:
        s1, s2, s3, s4, s5 = st.columns(5)
        with s1:
            st.metric("การจองทั้งหมด", stats.get("total_bookings", 0))
        with s2:
            st.metric("ยืนยันแล้ว", stats.get("confirmed", 0))
        with s3:
            st.metric("สำเร็จแล้ว", stats.get("completed", 0))
        with s4:
            st.metric("ยกเลิก", stats.get("cancelled", 0))
        with s5:
            st.metric("ยอดใช้จ่ายรวม", f"฿{stats.get('total_spent', 0):,.0f}")
    else:
        st.info("ยังไม่มีข้อมูลสถิติ")

# ── ประวัติการจอง ──
st.markdown("---")
st.subheader("📋 ประวัติการจอง")

bookings = booking_repo.get_user_bookings_detail(user_id)

if not bookings:
    st.info("ยังไม่มีประวัติการจอง")
else:
    # Filter
    status_filter = st.selectbox(
        "กรองตามสถานะ",
        ["ทั้งหมด", "pending_payment", "confirmed", "completed", "cancelled"],
        format_func=lambda x: {
            "ทั้งหมด": "ทั้งหมด", 
            "pending_payment": "รอชำระเงิน",
            "confirmed": "ยืนยันแล้ว", 
            "completed": "สำเร็จแล้ว", 
            "cancelled": "ยกเลิก"
        }.get(x, x),
    )

    if status_filter != "ทั้งหมด":
        bookings = [b for b in bookings if b["status"] == status_filter]

    status_icons = {"pending_payment": "💳", "confirmed": "🟡", "completed": "✅", "cancelled": "🔴"}
    status_text = {"pending_payment": "รอชำระเงิน", "confirmed": "ยืนยันแล้ว", "completed": "สำเร็จแล้ว", "cancelled": "ยกเลิก"}

    for b in bookings:
        with st.container():
            c1, c2, c3 = st.columns([2, 2, 1])

            with c1:
                st.write(f"**{b.get('camp_name', '-')}**")
                st.write(f"📍 {b.get('location', '-')}")

            with c2:
                if b.get("start_date"):
                    st.write(f"📅 วันเริ่ม: {b['start_date'].strftime('%d/%m/%Y')}")
                if b.get("duration"):
                    st.write(f"⏱️ ระยะเวลา: {b['duration']} วัน")
                if b.get("booked_at"):
                    st.write(f"📝 จองเมื่อ: {b['booked_at'].strftime('%d/%m/%Y')}")

            with c3:
                icon = status_icons.get(b.get("status"), "⚪")
                text = status_text.get(b.get("status"), b.get("status", "-"))
                st.write(f"{icon} {text}")
                if b.get("price"):
                    st.write(f"💰 ฿{b['price']:,}")

            st.markdown("---")