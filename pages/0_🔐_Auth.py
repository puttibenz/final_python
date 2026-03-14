import streamlit as st
from utils.auth import init_session_state, login, register

# Set page config
st.set_page_config(page_title="Auth - Camping Project", page_icon="🔐")
# Initialize session state for auth
init_session_state()

st.title("🔐 Account Access")

if st.session_state.is_logged_in:
    st.success(f"Welcome back, {st.session_state.username}!")
    if st.button("Logout"):
        from utils.auth import logout
        logout()
else:
    # Use tabs for Login and Register to keep it clean
    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        st.header("Login")
        with st.form("login_form"):
            l_username = st.text_input("Username")
            l_password = st.text_input("Password", type="password")
            l_submit = st.form_submit_button("Log In")
            
            if l_submit:
                if login(l_username, l_password):
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid username or password (try admin / password)")

    with tab2:
        st.header("Register")
        with st.form("register_form"):
            r_username = st.text_input("Username")
            r_email = st.text_input("Email")
            r_password = st.text_input("Password", type="password")
            r_confirm = st.text_input("Confirm Password", type="password")
            r_submit = st.form_submit_button("Sign Up")
            
            if r_submit:
                if r_password != r_confirm:
                    st.error("Passwords do not match.")
                elif register(r_username, r_password, r_email):
                    st.success("Registration successful! You can now log in.")
                else:
                    st.error("Please fill in all fields.")
