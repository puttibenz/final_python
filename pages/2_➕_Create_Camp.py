import streamlit as st
from components.forms import CampForm
from components.camp_card import CampCard
from utils.auth import check_auth_required, init_session_state
from database.crud import camp_repo
import time

# Set page configuration
st.set_page_config(page_title="Create Camp - Camping Project", page_icon="➕", layout="centered")

# Initialize Session State
init_session_state()

# --- Security: Only logged-in users can access this page ---
check_auth_required()

st.title("➕ Host a New Camping Trip")
st.markdown("""
Do you have an exciting trip idea? Share it with the community here.
Your trip will be visible on the Explore page immediately after publishing.
""")

# Layout: Form on the left, Preview on the right (if on wide mode) or Stacked
col1, col2 = st.columns([1.2, 1])

with col1:
    st.subheader("📝 Trip Details")
    # Instantiate the CampForm Class
    create_camp_form = CampForm()
    # Render the form UI and capture result
    new_camp_data = create_camp_form.render()

with col2:
    st.subheader("🖼️ Live Preview")
    st.info("This is how your trip will look to others:")
    
    # We use a placeholder to show the card based on form input (if form class allowed real-time access)
    # For now, we'll show a default preview or the data if submitted
    preview_data = new_camp_data if new_camp_data else {
        "name": "Your Awesome Trip Name",
        "location": "Province",
        "price": 0,
        "slots": 10,
        "contact": "Your Contact Info",
        "image": None
    }
    
    preview_card = CampCard(preview_data)
    preview_card.render()

# --- Database Submission Logic ---
if new_camp_data:
    with st.spinner("Publishing your adventure to the database..."):
        # Add metadata
        new_camp_data['created_by'] = st.session_state.get('username', 'anonymous')
        new_camp_data['created_at'] = time.strftime('%Y-%m-%d %H:%M:%S')
        
        result = camp_repo.create(new_camp_data)
        
        if result:
            st.success(f"🎉 '{new_camp_data['name']}' has been published successfully!")
            st.balloons()
            time.sleep(2)
            st.switch_page("pages/1_🏕️_Explore.py")
        else:
            st.error("❌ Failed to save to database. Please check your connection.")

# --- Help / Guide Sidebar ---
with st.sidebar:
    st.header("📋 Guide to Hosting")
    st.markdown("""
    **Tips for a great trip:**
    - **Attractive Name:** Make it stand out!
    - **Clear Dates:** Ensure they're correct.
    - **Fair Price:** Keep it competitive.
    - **Contact Info:** Essential for joining.
    - **Image:** Use a high-quality photo!
    """)
    st.divider()
    st.info("💡 Your data is now being saved directly to Supabase.")
