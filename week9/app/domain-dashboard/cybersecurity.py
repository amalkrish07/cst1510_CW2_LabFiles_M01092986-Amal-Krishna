import streamlit as st
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../week8')))
from app.data.db import connect_database
from app.data import incidents

def show_dashboard(st):
    conn = connect_database()
    st.title("🛡️ Cybersecurity Dashboard")

    all_inc = incidents.get_all_incidents(conn)
    high = all_inc[all_inc["severity"] == "High"]
    medium = all_inc[all_inc["severity"] == "Medium"]
    low = all_inc[all_inc["severity"] == "Low"]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("High Severity Incidents", len(high))
    with col2:
        st.metric("Medium Severity Incidents", len(medium))
    with col3:
        st.metric("Low Severity Incidents", len(low))

    st.header("Incident Type Distribution")
    type_counts = all_inc["incident_type"].value_counts()
    if not type_counts.empty:
        st.bar_chart(type_counts)
    else:
        st.info("No incident data available.")

    st.header("Severity Trend")
    severity_trend = all_inc.groupby("severity").size()
    if not severity_trend.empty:
        st.line_chart(severity_trend)
    else:
        st.info("No severity trend available.")

    st.success("Cybersecurity insights loaded successfully.")
