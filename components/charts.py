import streamlit as st
import pandas as pd

class AdminCharts:
    """Class สำหรับจัดการกราฟวิเคราะห์ข้อมูลสำหรับ Admin"""
    
    def __init__(self, bookings: list):
        if not bookings:
            self.df = pd.DataFrame()
        else:
            self.df = pd.DataFrame(bookings)
            # แปลงวันที่ให้เป็น datetime object
            if 'booked_at' in self.df.columns:
                self.df['booked_at'] = pd.to_datetime(self.df['booked_at'])
                self.df['date_only'] = self.df['booked_at'].dt.date

    def render_booking_status_pie(self):
        """กราฟวงกลมแสดงสัดส่วนสถานะการจอง"""
        if self.df.empty: return
        
        st.write("📊 สัดส่วนสถานะการจอง")
        status_counts = self.df['status'].value_counts()
        
        # แมปชื่อไทยสำหรับแสดงผล
        thai_status = {
            "pending_payment": "รอชำระเงิน",
            "confirmed": "ยืนยันแล้ว",
            "completed": "สำเร็จแล้ว",
            "cancelled": "ยกเลิก"
        }
        status_counts.index = [thai_status.get(s, s) for s in status_counts.index]
        
        st.plotly_chart({
            "data": [{"values": status_counts.values, "labels": status_counts.index, "type": "pie", "hole": .4}],
            "layout": {"margin": dict(l=20, r=20, t=20, b=20), "height": 300}
        }, use_container_width=True)

    def render_revenue_trend(self):
        """กราฟเส้นแสดงแนวโน้มรายได้สะสม"""
        if self.df.empty: return
        
        st.write("📈 แนวโน้มรายได้สะสม (Confirmed/Completed)")
        # กรองเฉพาะที่จ่ายเงินแล้ว
        paid_df = self.df[self.df['status'].isin(['confirmed', 'completed'])].copy()
        if paid_df.empty:
            st.info("ยังไม่มีรายได้ที่ยืนยันแล้ว")
            return
            
        paid_df = paid_df.sort_values('booked_at')
        paid_df['cumulative_revenue'] = paid_df['price'].cumsum()
        
        st.line_chart(paid_df, x='booked_at', y='cumulative_revenue')

    def render_top_camps_bar(self):
        """กราฟแท่งแสดงแคมป์ที่ยอดนิยมที่สุด (ตามจำนวนการจอง)"""
        if self.df.empty: return
        
        st.write("🏆 แคมป์ยอดนิยม (Top 5)")
        top_camps = self.df['camp_name'].value_counts().head(5)
        st.bar_chart(top_camps)

    def render_daily_bookings_area(self):
        """กราฟพื้นที่แสดงจำนวนการจองในแต่ละวัน"""
        if self.df.empty: return
        
        st.write("📅 จำนวนการจองรายวัน")
        daily_counts = self.df.groupby('date_only').size().reset_index(name='count')
        st.area_chart(daily_counts.set_index('date_only'))
