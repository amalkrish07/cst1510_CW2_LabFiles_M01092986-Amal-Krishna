import streamlit as st
from app.auth import login_user, register_new_user

st.set_page_config(page_title="Login", page_icon="🔐", layout="centered")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = ""

st.title("🔐 User Login")

if st.session_state.logged_in:
    st.success(f"Logged in as **{st.session_state.username}**")
    if st.button("Go to Dashboard"):
        st.switch_page("pages/1_Dashboard.py")
    st.stop()

tab_login, tab_register = st.tabs(["Login", "Register"])

with tab_login:
    st.subheader("Login to your account")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Log In", type="primary"):
        success, role = login_user(username, password)

        if success:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = role

            st.success("Login successful.")
            st.switch_page("pages/1_Dashboard.py")
        else:
            st.error("Invalid credentials. Please try again.")

with tab_register:
    st.subheader("Create a new account")

    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    confirm = st.text_input("Confirm Password", type="password")

    role = st.selectbox("Select Role", ["user", "admin", "analyst"])

    if st.button("Register"):
        if new_password != confirm:
            st.error("Passwords do not match.")
        else:
            success, msg = register_new_user(new_username, new_password, role)
            if success:
                st.success(msg)
            else:
                st.error(msg)
