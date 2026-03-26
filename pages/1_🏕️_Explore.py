import streamlit as st
from components.camp_card import CampCard
from database.crud import camp_repo

st.set_page_config(page_title="Explore Camps - Camping Project", page_icon="🏕️", layout="wide")

# Modern Header
st.title("🏕️ Discover Your Next Adventure")
st.markdown("Explore the best camping trips from across the community. Find, book, and explore.")

# Fetch Data from Supabase
@st.cache_data(ttl=600)  # Cache for 10 minutes
def load_camp_data():
    try:
        return camp_repo.get_all()
    except Exception as e:
        st.error(f"Failed to connect to Database: {e}")
        return []

camps_data = load_camp_data()

# --- Sidebar / Search & Filters ---
with st.sidebar:
    st.header("🔍 Search & Filter")
    search_query = st.text_input("Find by name or province", placeholder="e.g. Khao Kho")
    
    price_range = st.slider(
        "Max Price (฿)", 
        0, 10000, 10000, 
        step=500
    )
    
    st.divider()
    st.info("💡 Pro Tip: Filtered results update in real-time as you search.")

# --- Filter Logic ---
# Note: Using .get() and str conversion for safety in case some fields are missing in DB
filtered_data = [
    c for c in camps_data 
    if (search_query.lower() in str(c.get('name', '')).lower() or 
        search_query.lower() in str(c.get('location', '')).lower())
    and (float(c.get('price', 0)) <= price_range)
]

# --- Display Content using Classes ---
if not filtered_data:
    if not camps_data:
        st.info("No camping trips have been created yet. Be the first to host one!")
    else:
        st.warning("No trips found matching your criteria. Try widening your search!")
else:
    st.write(f"Showing **{len(filtered_data)}** upcoming trips.")
    
    # Create 3-column grid
    cols = st.columns(3)
    
    for index, data in enumerate(filtered_data):
        # Instantiate the CampCard Class for each trip
        camp_card = CampCard(data)
        
        with cols[index % 3]:
            # Use the Class method to render the UI
            camp_card.render()

# --- Footer ---
st.divider()
st.caption("© 2026 Camping Project Community | Data synced with Supabase Realtime Database")
