import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../week8')))
from app.data.db import connect_database
from app.data import tickets, schema

st.set_page_config(page_title="IT Tickets", page_icon="🎫", layout="wide")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must log in to access the Tickets page.")
    st.stop()

st.title("🎫 IT Tickets Dashboard")

conn = connect_database()

schema.create_it_tickets_table(conn)

with st.expander("➕ Add New Ticket"):
    st.subheader("Add New IT Ticket")
    with st.form("ticket_form", clear_on_submit=True):
        ticket_id = st.text_input("Ticket ID")
        priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        status = st.selectbox("Status", ["Open", "In Progress", "Closed"])
        category = st.text_input("Category")
        subject = st.text_input("Subject")
        description = st.text_area("Description")
        created_date = st.date_input("Created Date")
        resolved_date = st.date_input("Resolved Date", value=None)
        assigned_to = st.text_input("Assigned To")

        submitted = st.form_submit_button("Add Ticket")
        if submitted:
            tickets.insert_ticket(
                conn,
                ticket_id,
                priority,
                status,
                category,
                subject,
                description,
                str(created_date),
                str(resolved_date) if resolved_date else None,
                assigned_to if assigned_to else None
            )
            st.success(f"Ticket '{ticket_id}' added successfully!")

st.subheader("All IT Tickets")
df_tickets = tickets.get_all_tickets(conn)
st.dataframe(df_tickets)

with st.expander("✏️ Update Ticket"):
    st.subheader("Update Ticket Info")
    update_ticket_id = st.text_input("Ticket ID to Update", key="update_ticket_id")
    new_priority = st.selectbox("New Priority", ["Low", "Medium", "High"], key="new_priority")
    new_status = st.selectbox("New Status", ["Open", "In Progress", "Closed"], key="new_status")
    new_category = st.text_input("New Category", key="new_category")
    new_subject = st.text_input("New Subject", key="new_subject")
    new_description = st.text_area("New Description", key="new_description")
    new_assigned_to = st.text_input("New Assigned To", key="new_assigned_to")

    if st.button("Update Ticket"):
        rows_updated = tickets.update_ticket(
            conn,
            update_ticket_id,
            priority=new_priority,
            status=new_status,
            category=new_category,
            subject=new_subject,
            description=new_description,
            assigned_to=new_assigned_to
        )
        if rows_updated:
            st.success(f"Ticket '{update_ticket_id}' updated successfully!")
        else:
            st.error("Ticket ID not found.")

with st.expander("🗑️ Delete Ticket"):
    st.subheader("Delete Ticket")
    delete_ticket_id = st.text_input("Ticket ID to Delete", key="delete_ticket_id")
    if st.button("Delete Ticket"):
        rows_deleted = tickets.delete_ticket(conn, delete_ticket_id)
        if rows_deleted:
            st.success(f"Ticket '{delete_ticket_id}' deleted successfully.")
        else:
            st.error("Ticket ID not found.")
