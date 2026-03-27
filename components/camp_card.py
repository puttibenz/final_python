import streamlit as st


class CampCard:
    """Component แสดงการ์ดแคมป์ พร้อมปุ่มจอง"""

    def __init__(self, data: dict):
        self.data = data

    def render(self, booked=False, user_id=None):
        camp = self.data
        camp_id = camp.get("id", 0)
        name = camp.get("name", "ไม่มีชื่อ")
        location = camp.get("location", "-")
        price = camp.get("price", 0) or 0
        duration = camp.get("duration", "-")
        slots = camp.get("available_slots", camp.get("slots", 0)) or 0
        image_url = camp.get("image_url", "")
        description = camp.get("description", "")
        contact = camp.get("contact", "")
        start_date = camp.get("start_date", "")
        created_by = camp.get("created_by")

        with st.container():
            st.markdown(f"""
            <div style="border:1px solid #333; border-radius:16px; padding:1.2rem; 
                        background:#1E1E1E; margin-bottom:1rem;">
                <h3 style="margin:0 0 0.3rem; color:#66BB6A;">🏕️ {name}</h3>
                <p style="color:#aaa; margin:0 0 0.8rem; font-size:0.9rem;">📍 {location}</p>
            </div>
            """, unsafe_allow_html=True)

            if image_url:
                st.image(image_url, use_container_width=True)

            col1, col2, col3 = st.columns(3)
            col1.metric("💰 ราคา", f"฿{price:,.0f}")
            col2.metric("📅 จำนวนวัน", f"{duration} วัน")
            col3.metric("👥 เหลือ", f"{slots} คน")

            if start_date:
                st.caption(f"🗓️ เริ่ม: {start_date}")
            if description:
                with st.expander("📝 รายละเอียด"):
                    st.write(description)
            if contact:
                st.caption(f"📞 {contact}")

            # ── ปุ่มจอง ──
            if booked:
                st.success("✅ จองแล้ว")
            elif user_id and created_by == user_id:
                st.info("🏠 ทริปที่คุณสร้าง")
            elif slots <= 0:
                st.error("❌ เต็มแล้ว")
            else:
                if st.button(f"🎟️ จองทริปนี้", key=f"book_{camp_id}", use_container_width=True):
                    return camp_id  # ส่ง camp_id กลับให้หน้า Explore จัดการจอง

            st.markdown("---")
            return None