import streamlit as st
import json
import os
from components.camp_card import CampCard

st.set_page_config(page_title="Explore Camps - Camping Project", page_icon="🏕️", layout="wide")

# Modern Header
st.title("🏕️ Discover Your Next Adventure")
st.markdown("Explore the best camping trips from across the community. Find, book, and explore.")

# Load Data
@st.cache_data
def load_camp_data():
    file_path = 'data/camps.json'
    if not os.path.exists(file_path):
        return []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return []

camps_data = load_camp_data()

# --- Sidebar / Search & Filters ---
with st.sidebar:
    st.header("🔍 Search & Filter")
    search_query = st.text_input("Find by name or province", placeholder="e.g. Khao Kho")
    
    price_range = st.slider(
        "Max Price (฿)", 
        0, 10000, 5000, 
        step=500
    )
    
    st.divider()
    st.info("💡 Pro Tip: Filtered results update in real-time as you search.")

# --- Filter Logic ---
filtered_data = [
    c for c in camps_data 
    if (search_query.lower() in c['name'].lower() or search_query.lower() in c['location'].lower())
    and (c['price'] <= price_range)
]

# --- Display Content using Classes ---
if not filtered_data:
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
st.caption("© 2026 Camping Project Community | Data sourced from Facebook Community Groups")
