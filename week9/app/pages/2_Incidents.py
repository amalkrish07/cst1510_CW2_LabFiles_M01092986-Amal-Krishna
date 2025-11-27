import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../week8')))

from app.data.db import connect_database
from app.data import incidents

st.set_page_config(page_title="Incidents", page_icon="🛡️", layout="wide")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must log in to access the Incidents page.")
    st.stop()

st.title("🛡️ Cybersecurity Incidents")

conn = connect_database()

with st.expander("➕ Add New Incident"):
    st.subheader("Add New Incident")
    with st.form("incident_form", clear_on_submit=True):
        date = st.date_input("Incident Date")
        incident_type = st.text_input("Incident Type")
        severity = st.selectbox("Severity", ["Low", "Medium", "High"])
        status = st.selectbox("Status", ["Open", "In Progress", "Resolved"])
        description = st.text_area("Description")
        reported_by = st.text_input("Reported By")

        submitted = st.form_submit_button("Add Incident")
        if submitted:
            incidents.insert_incident(
                conn,
                date=str(date),
                incident_type=incident_type,
                severity=severity,
                status=status,
                description=description,
                reported_by=reported_by
            )
            st.success(f"Incident '{incident_type}' added successfully!")

st.subheader("All Incidents")
df_incidents = incidents.get_all_incidents(conn)
st.dataframe(df_incidents)

with st.expander("✏️ Update Incident Status"):
    st.subheader("Update Status")
    incident_id = st.number_input("Incident ID", min_value=1, step=1)
    new_status = st.selectbox("New Status", ["Open", "In Progress", "Resolved"])
    if st.button("Update Status"):
        updated = incidents.update_incident_status(conn, incident_id, new_status)
        if updated:
            st.success(f"Incident ID {incident_id} status updated to {new_status}.")
        else:
            st.error("Incident ID not found.")

with st.expander("🗑️ Delete Incident"):
    st.subheader("Delete Incident")
    delete_id = st.number_input("Incident ID to Delete", min_value=1, step=1, key="delete_id")
    if st.button("Delete Incident"):
        deleted = incidents.delete_incident(conn, delete_id)
        if deleted:
            st.success(f"Incident ID {delete_id} deleted successfully.")
        else:
            st.error("Incident ID not found.")
