import streamlit as st

st.set_page_config(page_title="Settings", page_icon="⚙️", layout="wide")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must log in to access the Settings page.")
    st.stop()

st.title("⚙️ Settings")
st.header("👤 Profile Information")

st.write(f"**Username:** {st.session_state.username}")
st.write(f"**Role:** {st.session_state.role}")

st.divider()

st.header("🚪 Account Actions")

if st.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""
    st.success("Logged out successfully! Redirecting...")
    st.switch_page("Home.py")
