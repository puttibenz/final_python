import streamlit as st


class CampCard:
    """Component แสดงการ์ดแคมป์ พร้อมปุ่มจอง"""

    def __init__(self, data: dict):
        self.data = data

    def render(self, booked=False, user_id=None):
        camp = self.data
        camp_id = camp.get("id", 0)
        name = camp.get("name", "ไม่มีชื่อ")
        location = camp.get("location", "ไทย")
        price = camp.get("price", 0) or 0
        duration = camp.get("duration", "-")
        slots = camp.get("available_slots", camp.get("slots", 0)) or 0
        image_url = camp.get("image_url", "")
        description = camp.get("description", "")
        contact = camp.get("contact", "")
        facebook_link = camp.get("facebook_link", "")
        start_date = camp.get("start_date", "")
        created_by = camp.get("created_by")

        # Define animation delay based on id or some variation
        anim_delay = (camp_id % 10) * 0.05

        st.markdown(f"""
        <style>
            .trip-card {{
                background: #1E1E1E;
                border-radius: 20px;
                border: 1px solid #333;
                overflow: hidden;
                box-shadow: 0 4px 20px rgba(0,0,0,0.3);
                transition: transform .25s, box-shadow .25s;
                height: 100%;
                display: flex; flex-direction: column;
                margin-bottom: 20px;
                animation: slideUp .45s {anim_delay}s ease both;
            }}
            .trip-card:hover {{
                transform: translateY(-5px);
                box-shadow: 0 12px 30px rgba(102,187,106,0.15);
                border-color: #66BB6A;
            }}
            .trip-img-wrap {{
                position: relative;
                height: 180px;
                background: #252525;
                overflow: hidden;
                flex-shrink: 0;
            }}
            .trip-img-wrap img {{
                width: 100%; height: 100%; object-fit: cover;
                transition: transform .4s ease;
            }}
            .trip-card:hover .trip-img-wrap img {{ transform: scale(1.08); }}
            
            .trip-location-badge {{
                position: absolute; bottom: 12px; left: 12px;
                background: rgba(0,0,0,.7);
                backdrop-filter: blur(8px);
                color: #fff; border-radius: 100px;
                padding: 4px 12px; font-size: .75rem; font-weight: 500;
                border: 1px solid rgba(255,255,255,.1);
            }}
            .trip-logo {{
                position: absolute; top: 12px; left: 12px;
                background: rgba(102,187,106,.9);
                border-radius: 10px; padding: 5px 8px;
                font-size: 1.1rem;
                border: 1px solid rgba(255,255,255,.2);
            }}
            .trip-body {{ padding: 15px; flex: 1; display: flex; flex-direction: column; gap: 10px; }}
            .trip-name {{ font-weight:600; font-size:1rem; color:#66BB6A; line-height:1.3; height: 2.6rem; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; }}
            
            .trip-meta-row {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; }}
            .trip-meta-box {{ background: #252525; border-radius: 10px; padding: 6px 4px; text-align: center; border: 1px solid #333; }}
            .trip-meta-label {{ font-size: .6rem; color: #888; text-transform: uppercase; margin-bottom: 2px; }}
            .trip-meta-value {{ font-size: .95rem; font-weight: 700; color: #fff; line-height: 1.1; }}
            .trip-meta-value.price {{ color: #66BB6A; }}
            .trip-meta-unit {{ font-size: .6rem; color: #666; }}
            
            .trip-info-line {{ font-size: .78rem; color: #aaa; display: flex; align-items: center; gap: 6px; }}
            .trip-info-line strong {{ color: #66BB6A; }}
        </style>

        <div class="trip-card">
            <div class="trip-img-wrap">
                <div class="trip-logo">⛺</div>
                {"<img src='"+image_url+"'>" if image_url else "<div style='width:100%;height:100%;display:flex;align-items:center;justify-content:center;font-size:3rem;opacity:.2;'>⛺</div>"}
                <div class="trip-location-badge">📍 {location}</div>
            </div>
            <div class="trip-body">
                <div class="trip-name">{name}</div>
                <div class="trip-meta-row">
                    <div class="trip-meta-box">
                        <div class="trip-meta-label">💰 ราคา</div>
                        <div class="trip-meta-value price">฿{price:,}</div>
                    </div>
                    <div class="trip-meta-box">
                        <div class="trip-meta-label">📅 วัน</div>
                        <div class="trip-meta-value">{duration}</div>
                        <div class="trip-meta-unit">วัน</div>
                    </div>
                    <div class="trip-meta-box">
                        <div class="trip-meta-label">👥 เหลือ</div>
                        <div class="trip-meta-value">{slots}</div>
                        <div class="trip-meta-unit">ที่</div>
                    </div>
                </div>
                <div class="trip-info-line">🗓️ เริ่ม: <strong>{start_date if start_date else "เร็วๆ นี้"}</strong></div>
                {f'<div class="trip-info-line">📞 {contact}</div>' if contact else '<div class="trip-info-line">📞 ไม่มีข้อมูล</div>'}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Functional Buttons (Streamlit Native) ──
        # Since HTML buttons in st.markdown can't trigger Python actions easily, 
        # we use Streamlit buttons below the card but style them to feel integrated.
        
        if created_by == 3:
            if facebook_link:
                st.link_button("🌐 ดูรายละเอียดบน Facebook", url=facebook_link, use_container_width=True)
            else:
                st.button("⚠️ ไม่พบลิงก์ Facebook", disabled=True, use_container_width=True)
        elif booked:
            st.success("✅ จองเรียบร้อยแล้ว")
        elif user_id and created_by == user_id:
            st.info("🏠 ทริปที่คุณสร้าง")
        elif slots <= 0:
            st.error("❌ ทริปนี้เต็มแล้ว")
        else:
            if st.button(f"🎟️ จองทริปนี้", key=f"bk_{camp_id}", use_container_width=True):
                return camp_id

        st.write("") # Spacer between cards
        return None