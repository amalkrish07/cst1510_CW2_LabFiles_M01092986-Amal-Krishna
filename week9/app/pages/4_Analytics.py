import streamlit as st
import pandas as pd
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../week8')))

from app.data.db import connect_database
from app.data import incidents, tickets

st.set_page_config(page_title="Analytics", page_icon="📈", layout="wide")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must log in to access Analytics.")
    st.stop()

st.title("📈 Analytics Dashboard")

conn = connect_database()

st.subheader("Select Domain")
domain = st.selectbox(
    "Choose analytics domain",
    ["Cybersecurity", "Data Science", "IT Operations"]
)

st.write(f"Showing analytics for **{domain}**")

st.header("Key Metrics")
col1, col2, col3 = st.columns(3)

total_incidents = len(incidents.get_all_incidents(conn))
total_tickets = len(tickets.get_all_tickets(conn))
high_sev_open = incidents.get_high_severity_by_status(conn)

with col1:
    st.metric("Total Incidents", total_incidents)

with col2:
    st.metric("Total Tickets", total_tickets)

with col3:
    st.metric(
        "High Severity Open",
        high_sev_open["count"].sum() if not high_sev_open.empty else 0,
        delta="+3"
    )

st.header("Incidents by Type")
incident_counts = incidents.get_incidents_by_type_count(conn)

if not incident_counts.empty:
    st.bar_chart(incident_counts.set_index("incident_type"))
else:
    st.info("No incident data available.")

st.header("Tickets by Status")

ticket_data = tickets.get_all_tickets(conn)
if not ticket_data.empty:
    status_counts = ticket_data["status"].value_counts()
    st.line_chart(status_counts)
else:
    st.info("No ticket data available.")

st.subheader("Domain Insights")

if domain == "Cybersecurity":
    st.info("⚠️ High-severity cybersecurity incidents detected. Review alert trends.")
elif domain == "Data Science":
    st.info("📊 Data processing workloads increasing. Monitor model performance.")
elif domain == "IT Operations":
    st.info("🖥️ System uptime stable. Track ticket resolution times.")
