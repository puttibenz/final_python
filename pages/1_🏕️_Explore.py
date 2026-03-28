import streamlit as st
from components.camp_card import CampCard
from database.crud import camp_repo, booking_repo
from utils.auth import auth_manager

st.set_page_config(page_title="Explore Camps", page_icon="🏕️", layout="wide")
auth_manager.check_auth_required()

# ── Custom CSS ──
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

# ── Dialogs ──
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
        booking_res = booking_repo.create_booking(user_id, camp['id'])
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

# เช็คว่ามีการจองค้างอยู่ที่ต้องจ่ายเงินไหม (หลังจากกด Yes ใน dialog แรก)
if "pending_booking" in st.session_state:
    pending = st.session_state.pop("pending_booking")
    payment_dialog(pending["id"], pending["name"], pending["price"])

# ── Sync Status ──
# อัปเดตสถานะแคมป์และการจองที่จบลงแล้วโดยอัตโนมัติ
camp_repo.sync_ended_camps()
booking_repo.sync_completed_bookings()

# ── Fetch Data ──
camps_data = camp_repo.get_all()
user_id = st.session_state.user["id"]
user_booked = booking_repo.get_user_bookings(user_id)

# ── Filter UI ──
with st.container():
    col_search, col_price = st.columns([2, 1])
    with col_search:
        search_query = st.text_input("🔍 ค้นหาชื่อหรือสถานที่", placeholder="เช่น เขาค้อ, กาญจนบุรี")
    with col_price:
        price_range = st.slider("💰 ราคาสูงสุด (฿)", 0, 10000, 10000, step=500)
    
    st.caption(f"📊 ทริปที่มีให้เลือก: {len(camps_data)} | จองแล้ว: {len(user_booked)}")
st.divider()

# ── Filter ──
filtered = [
    c for c in camps_data
    if (search_query.lower() in str(c.get("name", "")).lower()
        or search_query.lower() in str(c.get("location", "")).lower())
    and float(c.get("price", 0) or 0) <= price_range
    and c.get("status") == "active"
]

# ── Display Grid ──
if not filtered:
    if not camps_data:
        st.info("🏕️ ยังไม่มีทริปในระบบ — ลองสร้างทริปแรกของคุณ!")
    else:
        st.warning("ไม่พบทริปที่ตรงกับเงื่อนไข ลองปรับตัวกรองดู")
else:
    cols = st.columns(3)
    for idx, camp in enumerate(filtered):
        with cols[idx % 3]:
            card = CampCard(camp)
            is_booked = camp.get("id") in user_booked
            result = card.render(booked=is_booked, user_id=user_id)

            if result:
                confirm_booking_dialog(camp)

st.divider()
st.caption("© 2026 Camping Project Community")
