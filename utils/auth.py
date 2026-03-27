import streamlit as st

def init_session_state():
    """Initializes authentication variables in session state."""
    if "is_logged_in" not in st.session_state:
        st.session_state.is_logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = None

def login(username, password):
    """
    Mock login function. Replace this with a database check later.
    Currently accepts 'admin' / 'password' as a test.
    """
    if username == "admin" and password == "password":
        st.session_state.is_logged_in = True
        st.session_state.username = username
        return True
    return False

def logout():
    """Clears the session state and logs out the user."""
    st.session_state.is_logged_in = False
    st.session_state.username = None
    st.rerun()

def register(username, password, email):
    """
    Mock registration function. Replace this with database storage later.
    """
    if username and password and email:
        return True
    return False

def check_auth_required():
    """Call this on pages that require a login."""
    if not st.session_state.get("is_logged_in", False):
        st.warning("Please log in to access this page.")
        st.stop()
