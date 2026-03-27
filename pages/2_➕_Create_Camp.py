import streamlit as st
from components.forms import CampForm
from database.crud import camp_repo
from utils.auth import auth_manager

st.set_page_config(page_title="Create Camp", page_icon="➕", layout="centered")
auth_manager.check_auth_required()

# ── Custom CSS ──
st.markdown("""
<style>
    .camp-header {
        text-align: center;
        padding: 1.5rem 0 0.5rem;
    }
    .camp-header h1 {
        font-size: 2.2rem;
        background: linear-gradient(135deg, #2E7D32, #66BB6A);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .camp-header p {
        color: #888;
        font-size: 1rem;
    }
    div[data-testid="stForm"] {
        border: 1px solid #333;
        border-radius: 16px;
        padding: 2rem;
        background-color: #1E1E1E;
    }
    div[data-testid="stForm"] label {
        color: #FAFAFA !important;
        font-weight: 500 !important;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ──
st.markdown("""
<div class="camp-header">
    <h1>🏕️ สร้างทริปแคมป์ใหม่</h1>
    <p>กรอกรายละเอียดทริปของคุณ แล้วเผยแพร่ให้คนอื่นเข้าร่วม!</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ── Form (จาก component) ──
form = CampForm()
result = form.render()

if result:
    try:
        result["created_by"] = st.session_state.user["id"]
        camp_id = camp_repo.create(result)
        st.balloons()
        st.success(f"🎉 สร้างทริป **{result['name']}** สำเร็จ! (ID: {camp_id})")
    except Exception as e:
        st.error(f"❌ เกิดข้อผิดพลาด: {e}")

# ── แสดงทริปที่สร้างแล้ว ──
camps = camp_repo.get_all()
if camps:
    st.divider()
    st.subheader(f"📋 ทริปทั้งหมด ({len(camps)} ทริป)")
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