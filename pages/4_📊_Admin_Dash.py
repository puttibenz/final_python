import streamlit as st
from utils.auth import check_auth_required, init_session_state
from database.crud import camp_repo, booking_repo

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
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Camps", len(self.camps))
        with col2:
            st.metric("Total Bookings", "0") # Mock for now
        with col3:
            st.metric("Total Revenue", "฿0") # Mock for now

    def render_management(self):
        """Displays a table for managing camps."""
        st.subheader("📋 Camp Management")
        if not self.camps:
            st.info("No camps found in the database.")
        else:
            # Display as a table
            st.table(self.camps)

    def render(self):
        """Orchestrates the dashboard UI."""
        st.title("📊 Admin Dashboard (Mock Data Mode)")
        st.markdown("Welcome, Admin! Here you can monitor system activity and manage listings.")
        
        self.render_stats()
        st.divider()
        self.render_management()

# --- Page Setup ---
st.set_page_config(page_title="Admin Dash - Camping Project", page_icon="📊", layout="wide")

init_session_state()

# Security Check: Ensure only admin can access
# For now, let's just check if logged in (mock)
check_auth_required()

# Future: Add role-based check
# if st.session_state.user.get('role') != 'admin':
#     st.error("Access Denied: Admins only.")
#     st.stop()

# Instantiate and render
dashboard = AdminDashboard()
dashboard.render()
