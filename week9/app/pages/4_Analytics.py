import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from app.domain_dashboard.cybersecurity import show_dashboard as show_cybersec
from app.domain_dashboard.datascience import show_dashboard as show_ds
from app.domain_dashboard.itops import show_dashboard as show_itops

st.set_page_config(page_title="Analytics", page_icon="📈", layout="wide")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must log in to access Analytics.")
    st.stop()

st.title("📈 Analytics Dashboard")

domain = st.selectbox(
    "Choose analytics domain",
    ["Cybersecurity", "Data Science", "IT Operations"]
)

st.write(f"Showing analytics for **{domain}**")

if domain == "Cybersecurity":
    show_cybersec(st)
elif domain == "Data Science":
    show_ds(st)
elif domain == "IT Operations":
    show_itops(st)
