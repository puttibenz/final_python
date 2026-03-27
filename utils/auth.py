import streamlit as st

def init_session_state():
    """Initialize session state for auth."""
    if "is_logged_in" not in st.session_state:
        st.session_state.is_logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = None

def login(username, password):
    """Mock login function for development."""
    if username == "admin" and password == "password":
        st.session_state.is_logged_in = True
        st.session_state.username = username
        return True
    return False

def register(username, password, email):
    """Mock registration function."""
    if username and password and email:
        return True
    return False

def logout():
    """Clear session and rerun."""
    st.session_state.is_logged_in = False
    st.session_state.username = None
    st.rerun()

def check_auth_required():
    """Call this on pages that require a login."""
    if not st.session_state.get("is_logged_in", False):
        st.warning("Please log in to access this page.")
        st.stop()
