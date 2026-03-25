import streamlit as st
from datetime import datetime
from database.crud import camp_repo

class CampForm:
    """
    A class-based component to handle the Creation and Validation 
    of new Camping trips.
    """
    def __init__(self):
        self.data = {}
        self._initialize_fields()

    def _initialize_fields(self):
        """Sets up the initial state or default values for the form."""
        self.provinces = [
            "Chiang Mai", "Phetchabun", "Phetchaburi", "Kanchanaburi", 
            "Nakhon Nayok", "Chonburi", "Rayong", "Other"
        ]

    def render(self):
        """Renders the modern form UI in Streamlit."""
        st.markdown("### ⛺ Create Your Next Adventure")
        st.info("Fill in the details below to share your camping trip with the community.")

        with st.form("create_camp_form", clear_on_submit=False):
            # Layout with columns for a cleaner look
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Trip Name", placeholder="e.g. Starry Night at Khao Kho")
                location = st.selectbox("Province / Location", self.provinces)
                start_date = st.date_input("Start Date", min_value=datetime.now())
            
            with col2:
                price = st.number_input("Price per person (฿)", min_value=0, step=100)
                slots = st.number_input("Available Slots", min_value=1, step=1)
                duration = st.number_input("Duration (Days)", min_value=1, step=1)

            image_url = st.text_input("Image URL (Optional)", 
                                     placeholder="https://images.unsplash.com/photo-...")
            
            contact = st.text_input("Contact Info (Line, FB, or Phone)", 
                                   placeholder="e.g. FB: MyCampingPage / Line: @camp123")
            
            description = st.text_area("Detailed Description", 
                                      placeholder="Describe the activities, equipment needed, and meeting point...")

            st.divider()
            
            # Form submission
            submit_btn = st.form_submit_button("🚀 Create Camp Trip", use_container_width=True)

            if submit_btn:
                self.data = {
                    "name": name,
                    "location": location,
                    "start_date": str(start_date),
                    "price": price,
                    "slots": slots,
                    "duration": duration,
                    "image": image_url if image_url else "https://images.unsplash.com/photo-1504280390367-361c6d9f38f4",
                    "contact": contact,
                    "description": description,
                    "created_at": str(datetime.now())
                }
                return self._handle_submission()
        
        return None

    def _handle_submission(self):
        """Validates and processes the submitted data."""
        if not self.data["name"] or not self.data["contact"]:
            st.error("Please provide at least a Trip Name and Contact Info.")
            return None
        
        # Save to Supabase using the Repository
        result = camp_repo.create(self.data)
        
        if result:
            st.balloons()
            st.success(f"🎉 Successfully created '{self.data['name']}' in the database!")
            
            with st.expander("View Saved Data"):
                st.json(result.data)
            return self.data
        else:
            st.error("❌ Failed to save to database. Please check your Supabase connection and table settings.")
            return None
