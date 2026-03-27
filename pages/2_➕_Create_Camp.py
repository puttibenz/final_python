import streamlit as st
from components.forms import CampForm

st.set_page_config(page_title="Create Camp", page_icon="➕", layout="centered")

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
    # Mock: เก็บลง session_state (จะเปลี่ยนเป็น database จริงตอน merge)
    if "mock_camps" not in st.session_state:
        st.session_state.mock_camps = []
    st.session_state.mock_camps.append(result)

    st.balloons()
    st.success(f"🎉 สร้างทริป **{result['name']}** สำเร็จ!")

    with st.expander("📄 ดูข้อมูลที่ส่ง", expanded=False):
        st.json(result)

# ── แสดงทริปที่สร้างแล้ว (Mock) ──
if st.session_state.get("mock_camps"):
    st.divider()
    st.subheader(f"📋 ทริปที่สร้างแล้ว ({len(st.session_state.mock_camps)} ทริป)")
    for i, camp in enumerate(reversed(st.session_state.mock_camps)):
        with st.expander(f"🏕️ {camp['name']} — {camp['location']} | ฿{camp['price']:,}/คน"):
            col1, col2, col3 = st.columns(3)
            col1.metric("📅 วันเริ่ม", camp["start_date"])
            col2.metric("⏱️ จำนวนวัน", f"{camp['duration']} วัน")
            col3.metric("👥 รับได้", f"{camp['slots']} คน")
            if camp.get("description"):
                st.write(camp["description"])
            if camp.get("contact"):
                st.caption(f"📞 {camp['contact']}")