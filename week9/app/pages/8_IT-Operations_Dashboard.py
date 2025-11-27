import streamlit as st
import pandas as pd
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../week8')))

from app.data.db import connect_database
from app.data import incidents, tickets

st.set_page_config(page_title="IT Operations Dashboard", page_icon="🖥️", layout="wide")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must log in to access this page.")
    st.stop()

st.title("🖥️ IT Operations Dashboard")

conn = connect_database()

st.header("Ops Metrics")

inc = incidents.get_all_incidents(conn)
tix = tickets.get_all_tickets(conn)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Incidents", len(inc))

with col2:
    critical = inc[inc["severity"] == "High"]
    st.metric("Critical Incidents", len(critical))

with col3:
    pending = tix[tix["status"] == "Open"]
    st.metric("Pending Tickets", len(pending))

st.header("Incidents by Type")
type_counts = inc["incident_type"].value_counts()

if not type_counts.empty:
    st.bar_chart(type_counts)
else:
    st.info("No incident type data.")

st.header("Incident vs Tickets Trend")

trend = pd.DataFrame({
    "Incidents": [len(inc)],
    "Tickets": [len(tix)]
})

st.line_chart(trend)

st.success("IT Operations insights loaded successfully.")
