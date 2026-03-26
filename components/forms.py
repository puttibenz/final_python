import streamlit as st
from datetime import datetime

class CampForm:
    """A class-based component to handle the Creation and Validation (Mock)."""
    def __init__(self):
        self.data = {}
        self.provinces = ["Chiang Mai", "Phetchabun", "Phetchaburi", "Other"]

    def render(self):
        st.markdown("### ⛺ Create Your Next Adventure (Mock Mode)")
        with st.form("create_camp_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Trip Name")
                location = st.selectbox("Province", self.provinces)
            with col2:
                price = st.number_input("Price", min_value=0)
                slots = st.number_input("Slots", min_value=1)
            
            contact = st.text_input("Contact Info")
            submit_btn = st.form_submit_button("🚀 Create Camp (Simulated)", use_container_width=True)

            if submit_btn:
                self.data = {"name": name, "location": location, "price": price, "slots": slots, "contact": contact}
                st.balloons()
                st.success(f"🎉 Simulated creation of '{name}' successful!")
                st.json(self.data)
                return self.data
        return None
