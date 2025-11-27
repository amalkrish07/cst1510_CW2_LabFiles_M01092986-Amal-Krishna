import streamlit as st
import pandas as pd
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../week8')))
from app.data.db import connect_database
from app.data import tickets

def show_dashboard(st):
    conn = connect_database()
    st.title("📊 Data Science Dashboard")

    all_tickets = tickets.get_all_tickets(conn)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Tickets", len(all_tickets))
    with col2:
        open_tickets = all_tickets[all_tickets["status"] == "Open"]
        st.metric("Open Tickets", len(open_tickets))
    with col3:
        closed_tickets = all_tickets[all_tickets["status"] == "Closed"]
        st.metric("Closed Tickets", len(closed_tickets))

    st.header("Ticket Status Breakdown")
    status_counts = all_tickets["status"].value_counts()
    if not status_counts.empty:
        st.bar_chart(status_counts)
    else:
        st.info("No ticket data to visualize.")

    st.header("Ticket Volume Trend")
    ticket_trend = all_tickets.groupby("priority").size()
    if not ticket_trend.empty:
        st.line_chart(ticket_trend)
    else:
        st.info("No trend data available.")

    st.success("Data Science insights loaded successfully.")
