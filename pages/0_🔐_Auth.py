import streamlit as st
from utils.auth import init_session_state, login, register, logout

st.set_page_config(page_title="Auth - Camping Project", page_icon="🔐", layout="centered")

init_session_state()

st.title("🔐 Account Access (Mock System)")

if st.session_state.is_logged_in:
    st.success(f"Welcome back, **{st.session_state.username}**!")
    if st.button("🚪 Logout", use_container_width=True):
        logout()
else:
    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        st.header("Login")
        with st.form("login_form"):
            l_username = st.text_input("Username", value="admin")
            l_password = st.text_input("Password", type="password", value="password")
            l_submit = st.form_submit_button("🚀 Log In", use_container_width=True)
            
            if l_submit:
                if login(l_username, l_password):
                    st.success("Success! (Mock Login)")
                    st.rerun()
                else:
                    st.error("Invalid username or password.")

    with tab2:
        st.header("Create Account")
        with st.form("register_form"):
            r_username = st.text_input("Username")
            r_email = st.text_input("Email Address")
            r_password = st.text_input("Password", type="password")
            r_confirm = st.text_input("Confirm Password", type="password")
            r_submit = st.form_submit_button("✨ Sign Up", use_container_width=True)
            
            if r_submit:
                if r_password != r_confirm:
                    st.error("Passwords do not match.")
                elif register(r_username, r_password, r_email):
                    st.success("✅ Mock Registration successful! Now try logging in.")
