import streamlit as st
import json
import os
from components.camp_card import CampCard
from database.crud import camp_repo

st.set_page_config(page_title="Explore Camps - Camping Project", page_icon="🏕️", layout="wide")

# Modern Header
st.title("🏕️ Discover Your Next Adventure")
st.markdown("Explore the best camping trips from across the community. Find, book, and explore.")

# Load Data from Supabase
@st.cache_data(ttl=600) # Cache for 10 minutes
def load_camp_data():
    data = camp_repo.get_all()
    if not data:
        # Fallback to local mock data if database is empty or not connected
        file_path = 'data/camps.json'
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
    return data

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
    
    if st.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()

    st.divider()
    st.info("💡 Pro Tip: Results are fetched live from Supabase.")

# --- Filter Logic ---
filtered_data = [
    c for c in camps_data 
    if (search_query.lower() in c['name'].lower() or search_query.lower() in (c.get('location') or "").lower())
    and (c.get('price', 0) <= price_range)
]

# --- Display Content ---
if not filtered_data:
    st.warning("No trips found matching your criteria. Try widening your search!")
else:
    st.write(f"Showing **{len(filtered_data)}** upcoming trips.")
    
    # Create 3-column grid
    cols = st.columns(3)
    
    for index, data in enumerate(filtered_data):
        camp_card = CampCard(data)
        with cols[index % 3]:
            camp_card.render()

# --- Footer ---
st.divider()
st.caption("© 2026 Camping Project Community | Powered by Supabase & Streamlit")
