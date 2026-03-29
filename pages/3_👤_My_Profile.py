import streamlit as st
from utils.auth import auth_manager
from database.crud import user_repo, booking_repo, camp_repo
from utils.base_page import BasePage

class ProfilePage(BasePage):
    """Class สำหรับจัดการหน้าโปรไฟล์ผู้ใช้ ตามแบบ imagej1 และ imagej2"""

    def __init__(self):
        super().__init__(title="👤 โปรไฟล์", subtitle="จัดการข้อมูลส่วนตัวของคุณ", require_auth=True)
        
        # โหลดข้อมูลล่าสุด
        self.latest_user = user_repo.get_user_by_id(self.user_id)
        self.stats = booking_repo.get_user_stats(self.user_id)

    def render_header(self):
        """Inject CSS สำหรับ Layout ใหม่ทั้งหมด"""
        # เรียก CSS พื้นฐาน
        self.render_common_css()
        
        st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&display=swap');
            
            /* Main Container Fixes */
            .main-content {
                max-width: 800px;
                margin: auto;
            }

            /* Profile Card (Top) */
            .profile-card {
                background: #FFFFFF;
                border-radius: 24px;
                padding: 3rem 2rem;
                text-align: center;
                border: 1px solid #E8F5E9;
                box-shadow: 0 4px 20px rgba(0,0,0,0.02);
                margin-bottom: 1.5rem;
            }
            .avatar-ring {
                width: 120px;
                height: 120px;
                border-radius: 50%;
                border: 2px solid #66BB6A;
                padding: 5px;
                margin: 0 auto 1.5rem;
                display: flex;
                align-items: center;
                justify-content: center;
                position: relative;
            }
            .avatar-ring::after {
                content: '';
                position: absolute;
                bottom: 10px;
                right: 10px;
                width: 15px;
                height: 15px;
                background: #66BB6A;
                border: 3px solid white;
                border-radius: 50%;
            }
            .profile-name {
                font-family: 'Playfair Display', serif;
                font-size: 2.5rem;
                color: #2E7D32;
                margin: 0;
                line-height: 1;
            }
            .profile-handle {
                color: #888;
                font-size: 1.1rem;
                margin: 0.5rem 0 1rem;
            }
            .role-badge {
                background: #E8F5E9;
                color: #2E7D32;
                padding: 4px 16px;
                border-radius: 20px;
                font-size: 0.8rem;
                font-weight: 600;
                display: inline-block;
            }

            /* Info Card */
            .info-card {
                background: #FFFFFF;
                border-radius: 24px;
                padding: 2rem;
                border: 1px solid #F1F8E9;
                margin-bottom: 1.5rem;
            }
            .section-header {
                display: flex;
                align-items: center;
                margin-bottom: 1.5rem;
            }
            .section-header h3 {
                margin: 0 1rem 0 0;
                color: #333;
                font-size: 1.2rem;
                white-space: nowrap;
            }
            .header-line {
                flex-grow: 1;
                height: 1px;
                background: #EEE;
            }
            .info-row {
                display: flex;
                align-items: center;
                margin-bottom: 1rem;
            }
            .info-icon {
                width: 45px;
                height: 45px;
                background: #F1F8E9;
                border-radius: 12px;
                display: flex;
                align-items: center;
                justify-content: center;
                margin-right: 1rem;
                font-size: 1.2rem;
            }
            .info-text p {
                margin: 0;
                font-size: 0.8rem;
                color: #888;
            }
            .info-text b {
                font-size: 1rem;
                color: #333;
            }

            /* Wallet Card */
            .wallet-card {
                background: linear-gradient(135deg, #2E7D32 0%, #1B5E20 100%);
                border-radius: 24px;
                padding: 2rem;
                color: white;
                margin-bottom: 1.5rem;
                position: relative;
                overflow: hidden;
            }
            .wallet-card::before {
                content: '';
                position: absolute;
                top: -50px;
                right: -50px;
                width: 200px;
                height: 200px;
                background: rgba(255,255,255,0.05);
                border-radius: 50%;
            }
            .wallet-label {
                font-size: 0.9rem;
                text-transform: uppercase;
                letter-spacing: 1px;
                opacity: 0.9;
                display: flex;
                align-items: center;
                margin-bottom: 1rem;
            }
            .wallet-amount {
                font-family: 'Playfair Display', serif;
                font-size: 3.5rem;
                margin: 0;
                display: flex;
                align-items: flex-start;
            }
            .currency-symbol {
                font-size: 1.5rem;
                margin-right: 5px;
                margin-top: 10px;
            }

            /* Stats Grid */
            .stats-container {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 1rem;
                margin-bottom: 1.5rem;
            }
            .stat-box {
                background: #FFFFFF;
                border-radius: 20px;
                padding: 1.5rem;
                text-align: center;
                border: 1px solid #F1F8E9;
            }
            .stat-label {
                color: #888;
                font-size: 0.8rem;
                margin-bottom: 0.5rem;
            }
            .stat-value {
                font-family: 'Playfair Display', serif;
                font-size: 2rem;
                color: #333;
                margin: 0.2rem 0;
            }
            .stat-unit {
                font-size: 0.7rem;
                color: #AAA;
            }

            /* Custom Tab Bar */
            .custom-tabs {
                display: flex;
                background: #FFFFFF;
                border-radius: 16px;
                padding: 6px;
                margin-bottom: 1rem;
                border: 1px solid #EEE;
            }
            .tab-item {
                flex: 1;
                text-align: center;
                padding: 10px;
                border-radius: 12px;
                cursor: pointer;
                font-weight: 500;
                transition: 0.3s;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 8px;
            }
            .tab-active {
                background: #2E7D32;
                color: white;
                box-shadow: 0 4px 10px rgba(46,125,50,0.2);
            }
            .tab-inactive {
                color: #666;
            }
        </style>
        """, unsafe_allow_html=True)

    def render_user_card(self):
        """การ์ดโปรไฟล์ส่วนบน"""
        st.markdown(f"""
        <div class="profile-card">
            <div class="avatar-ring">
                <span style="font-size: 60px;">👦</span>
            </div>
            <h1 class="profile-name">{self.user.get('username')}</h1>
            <p class="profile-handle">@{self.user.get('username')}</p>
            <div class="role-badge">● {self.user.get('role', 'user').upper()}</div>
        </div>
        """, unsafe_allow_html=True)

    def render_info_section(self):
        """ส่วนข้อมูลส่วนตัวและ Wallet"""
        # ข้อมูลส่วนตัว
        st.markdown(f"""
        <div class="info-card">
            <div class="section-header">
                <h3>ข้อมูลส่วนตัว</h3>
                <div class="header-line"></div>
            </div>
            <div class="info-row">
                <div class="info-icon">📧</div>
                <div class="info-text">
                    <p>อีเมล</p>
                    <b>{self.user.get('email', '-')}</b>
                </div>
            </div>
            <div class="info-row">
                <div class="info-icon">📞</div>
                <div class="info-text">
                    <p>โทรศัพท์</p>
                    <b>{self.user.get('phone', '-')}</b>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Wallet
        balance = self.latest_user.get("balance", 0) if self.latest_user else 0
        st.markdown(f"""
        <div class="wallet-card">
            <div class="wallet-label">💼 ยอดเงินคงเหลือ (WALLET)</div>
            <div class="wallet-amount">
                <span class="currency-symbol">฿</span>{balance:,.2f}
            </div>
        </div>
        """, unsafe_allow_html=True)

    def render_stats_grid(self):
        """ส่วนสถิติ (2x2)"""
        st.markdown("""
        <div class="info-card" style="padding-bottom: 1rem;">
            <div class="section-header">
                <h3>ความสำเร็จและสถิติ</h3>
                <div class="header-line"></div>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-label">จองทั้งหมด</div>
                <div class="stat-value">{self.stats.get('total_bookings', 0)}</div>
                <div class="stat-unit">ครั้ง</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"""
            <div class="stat-box" style="margin-top:1rem;">
                <div class="stat-label">รอยืนยัน</div>
                <div class="stat-value" style="color: #F57C00;">{self.stats.get('confirmed', 0)}</div>
                <div class="stat-unit">รายการ</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-label">ไปมาแล้ว</div>
                <div class="stat-value" style="color: #2E7D32;">{self.stats.get('completed', 0)}</div>
                <div class="stat-unit">แห่ง</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"""
            <div class="stat-box" style="margin-top:1rem;">
                <div class="stat-label">จ่ายสะสม</div>
                <div class="stat-value">฿{self.stats.get('total_spent', 0):,.0f}</div>
                <div class="stat-unit">บาท</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

    def render_tabs_content(self):
        """ส่วนแสดงประวัติการจองและแคมป์ที่สร้าง (ใช้ Tab ของ Streamlit แต่ปรับแต่งสไตล์)"""
        tab_booking, tab_my_camps = st.tabs(["📋 ประวัติการจอง", "🏕️ แคมป์ที่ฉันสร้าง"])

        with tab_booking:
            self._render_booking_history()

        with tab_my_camps:
            self._render_my_created_camps()

    def _render_booking_history(self):
        bookings = booking_repo.get_user_bookings_detail(self.user_id)
        if not bookings:
            st.markdown("""
            <div style="text-align:center; padding: 4rem 2rem; background:white; border-radius:24px; border:1px solid #EEE; margin-top:1rem;">
                <div style="font-size: 4rem; opacity: 0.2; margin-bottom: 1rem;">🗓️</div>
                <h3 style="color:#333; margin:0;">ยังไม่มีประวัติการจอง</h3>
                <p style="color:#888;">การจองของคุณจะปรากฏที่นี่</p>
            </div>
            """, unsafe_allow_html=True)
            return

        # Status filter simplified for clean UI
        status_filter = st.selectbox("กรองสถานะ", ["ทั้งหมด", "pending_payment", "confirmed", "completed", "cancelled"], format_func=lambda x: {"ทั้งหมด":"ทั้งหมด", "pending_payment":"รอชำระเงิน", "confirmed":"ยืนยันแล้ว", "completed":"สำเร็จแล้ว", "cancelled":"ยกเลิก"}.get(x,x))
        if status_filter != "ทั้งหมด":
            bookings = [b for b in bookings if b["status"] == status_filter]

        for b in bookings:
            st.markdown(f"""
            <div class="info-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <b style="font-size:1.1rem; color:#2E7D32;">{b.get('camp_name')}</b><br>
                        <small style="color:#888;">📍 {b.get('location')}</small>
                    </div>
                    <div style="text-align:right;">
                        <span class="role-badge" style="background:#F1F8E9;">{b.get('status').upper()}</span><br>
                        <b style="color:#333;">฿{b.get('price'):,}</b>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    def _render_my_created_camps(self):
        my_camps = camp_repo.get_camps_by_owner(self.user_id)
        if not my_camps:
            st.info("คุณยังไม่ได้สร้างแคมป์ใดๆ")
            return

        for camp in my_camps:
            with st.expander(f"🏕️ {camp['name']}"):
                st.write(f"สถานะ: {camp.get('status')}")
                if st.button("🗑️ ยกเลิกทริปนี้", key=f"del_{camp['id']}"):
                    if camp_repo.delete_camp(camp['id']):
                        st.rerun()

    def render(self):
        """Main Render Function"""
        self.render_header()
        
        # จัด Layout ให้อยู่ตรงกลางเหมือนในรูป
        _, main_col, _ = st.columns([1, 6, 1])
        
        with main_col:
            self.render_user_card()
            self.render_info_section()
            self.render_stats_grid()
            self.render_tabs_content()

if __name__ == "__main__":
    page = ProfilePage()
    page.render()
