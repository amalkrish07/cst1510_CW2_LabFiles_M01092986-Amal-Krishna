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

st.header(f"{domain} Analytics")

if domain == "Cybersecurity":
    st.subheader("Cyber Threat Insights")
    st.info("⚠️ High-severity cybersecurity incidents detected. Review alert trends.")

    if "type" in incident_counts.columns:
        cyber_data = incident_counts[incident_counts["incident_type"] == "cybersecurity"]
        if not cyber_data.empty:
            st.bar_chart(cyber_data.set_index("incident_type"))
        else:
            st.warning("No cybersecurity-specific incident data found.")

elif domain == "Data Science":
    st.subheader("Data Pipeline Insights")
    st.info("📊 Data processing workloads increasing. Monitor model performance.")

    performance_data = pd.DataFrame({
        "accuracy": [0.78, 0.82, 0.88, 0.91],
        "loss": [0.44, 0.39, 0.31, 0.22]
    })
    st.line_chart(performance_data)

elif domain == "IT Operations":
    st.subheader("IT Ops Insights")
    st.info("🖥️ System uptime stable. Track ticket resolution times.")

    if not ticket_data.empty:
        if "resolution_time" in ticket_data.columns:
            st.bar_chart(ticket_data["resolution_time"])
        else:
            st.warning("Resolution time data not found.")
