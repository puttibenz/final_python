import streamlit as st
from utils.auth import init_session_state, check_auth_required
from database.crud import camp_repo, booking_repo

# Page Config
st.set_page_config(page_title="Admin Dashboard", page_icon="📊", layout="wide")

init_session_state()
check_auth_required()

# Security Check: Ensure only admin can access
user = st.session_state.user
if user.get("role") != "admin":
    st.error("⛔ คุณไม่มีสิทธิ์เข้าถึงหน้านี้")
    st.stop()

class AdminDashboard:
    """
    A class-based component for the Admin Dashboard.
    Handles stats visualization and camp management.
    """
    def __init__(self):
        self.camps = camp_repo.get_all()
        self.bookings = [] # Future: booking_repo.get_all()

    def render_stats(self):
        """Displays high-level metrics."""
        st.subheader("📈 System Overview")
        # Example stats
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Camps", len(self.camps))
        col2.metric("Total Bookings", 0) # Mock
        col3.metric("Revenue", "$0") # Mock

    def render(self):
        st.title("📊 Admin Dashboard")
        self.render_stats()
        # Additional admin logic here...

# Instantiate and render
dashboard = AdminDashboard()
dashboard.render()
