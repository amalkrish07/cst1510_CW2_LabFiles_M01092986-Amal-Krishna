import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../week8')))

from app.data.db import connect_database
from app.data import incidents, tickets

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = ""
if not st.session_state.logged_in:
    st.error("You must log in to access the dashboard.")
    st.stop()

st.title("📊 Dashboard")
st.success(f"Welcome, {st.session_state.username} ({st.session_state.role})")

conn = connect_database()

st.header("Summary Metrics")
col1, col2, col3 = st.columns(3)

with col1:
    total_incidents = len(incidents.get_all_incidents(conn))
    st.metric("Total Incidents", total_incidents)

with col2:
    total_tickets = len(tickets.get_all_tickets(conn))
    st.metric("Total Tickets", total_tickets)

with col3:
    high_sev = incidents.get_high_severity_by_status(conn)
    st.metric("High Severity Open", high_sev["count"].sum() if not high_sev.empty else 0)

st.header("Incidents by Type")
incident_counts = incidents.get_incidents_by_type_count(conn)
if not incident_counts.empty:
    st.bar_chart(incident_counts.set_index("incident_type"))

with st.expander("All Incidents"):
    st.dataframe(incidents.get_all_incidents(conn))
