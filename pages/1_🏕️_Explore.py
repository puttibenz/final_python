import streamlit as st
from components.camp_card import CampCard
from database.crud import camp_repo, booking_repo
from utils.auth import init_session_state, check_auth_required

st.set_page_config(page_title="Explore Camps", page_icon="🏕️", layout="wide")
init_session_state()
check_auth_required()

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

# ── Fetch Data ──
camps_data = camp_repo.get_all()
user_id = st.session_state.user["id"]
user_booked = booking_repo.get_user_bookings(user_id)

# ── Sidebar Filters ──
with st.sidebar:
    st.header("🔍 ค้นหา & กรอง")
    search_query = st.text_input("ค้นหาชื่อหรือสถานที่", placeholder="เช่น เขาค้อ")
    price_range = st.slider("ราคาสูงสุด (฿)", 0, 10000, 10000, step=500)
    st.divider()
    st.caption(f"📊 ทริปทั้งหมด: {len(camps_data)} | จองแล้ว: {len(user_booked)}")

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
            result = card.render(booked=is_booked)

            if result:
                booking = booking_repo.create_booking(user_id, result)
                if booking and not isinstance(booking, dict):
                    st.success(f"🎉 จองสำเร็จ!")
                    st.rerun()
                else:
                    err = booking.get("error", "Unknown") if isinstance(booking, dict) else "Unknown"
                    st.error(f"❌ จองไม่สำเร็จ: {err}")

st.divider()
st.caption("© 2026 Camping Project Community")
