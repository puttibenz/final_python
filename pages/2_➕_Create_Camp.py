import streamlit as st
from components.forms import CampForm
from utils.auth import check_auth_required, init_session_state

# Set page configuration
st.set_page_config(page_title="Create Camp - Camping Project", page_icon="➕", layout="centered")

# Initialize Session State (in case user lands here directly)
init_session_state()

# --- Security: Only logged-in users can access this page ---
check_auth_required()

st.title("➕ Host a New Camping Trip")
st.markdown("""
Do you have an exciting trip idea? Share it with the community here.
""")

# Instantiate the CampForm Class (OOP)
create_camp_form = CampForm()

# Render the form UI and capture result
new_camp_data = create_camp_form.render()

# --- Post-Creation Logic (Optional) ---
if new_camp_data:
    # This block executes after the form has been successfully submitted and validated
    st.info("You can view your new trip in the 'Explore' page after it's approved by admin.")
    
    # You could potentially redirect them to another page after a few seconds
    # time.sleep(2)
    # st.switch_page("pages/1_🏕️_Explore.py")

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
    st.warning("⚠️ Any trip that doesn't follow community guidelines will be removed.")
