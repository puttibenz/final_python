import streamlit as st
from utils.auth import init_session_state, check_auth_required

st.set_page_config(page_title="Create Camp - Camping Project", page_icon="➕", layout="centered")
init_session_state()
check_auth_required()

st.title("➕ Create Camp")
st.info("🚧 This feature is under development. Stay tuned!")
