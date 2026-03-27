import streamlit as st
import json
import os
from components.camp_card import CampCard
from utils.auth import init_session_state, check_auth_required

st.set_page_config(page_title="Explore Camps - Camping Project", page_icon="🏕️", layout="wide")
init_session_state()
check_auth_required()

st.title("🏕️ Discover Your Next Adventure")
st.markdown("Explore the best camping trips from across the community. (Mock Data Mode)")

# Load Data from local JSON
@st.cache_data
def load_camp_data():
    file_path = 'data/camps.json'
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

camps_data = load_camp_data()

# --- Sidebar / Search & Filters ---
with st.sidebar:
    st.header("🔍 Search & Filter")
    search_query = st.text_input("Find by name or province")
    price_range = st.slider("Max Price (฿)", 0, 10000, 10000, step=500)

# --- Filter Logic ---
filtered_data = [
    c for c in camps_data 
    if (search_query.lower() in c['name'].lower() or search_query.lower() in c['location'].lower())
    and (c['price'] <= price_range)
]

# --- Display Grid ---
if not filtered_data:
    st.warning("No trips found matching your criteria.")
else:
    cols = st.columns(3)
    for index, data in enumerate(filtered_data):
        camp_card = CampCard(data)
        with cols[index % 3]:
            camp_card.render()

st.divider()
st.caption("Note: Currently showing mock data for development purposes.")
