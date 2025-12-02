import streamlit as st
from app.db_files.db import connect_database
from app.db_files import tickets
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

system_prompt = """You are a data science expert assistant.
Help with analysis, visualization, and statistical insights."""

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

    if "data_messages" not in st.session_state:
        st.session_state.data_messages = []

    with st.sidebar:
        st.header("Data Science AI Assistant")

        if st.button("Clear Chat"):
            st.session_state.data_messages = []

        user_input = st.text_input("Ask AI about tickets or analysis:")

        if st.button("Send"):
            if user_input:
                st.session_state.data_messages.append({"role": "user", "content": user_input})
                response = client.chat.completions.create(
                    model="gpt-4.1-mini",
                    messages=[{"role": "system", "content": system_prompt}, *st.session_state.data_messages]
                )
                reply = response.choices[0].message.content
                st.session_state.data_messages.append({"role": "assistant", "content": reply})

        for msg in st.session_state.data_messages:
            if msg["role"] == "user":
                st.markdown(f"**You:** {msg['content']}")
            else:
                st.markdown(f"**AI:** {msg['content']}")

    st.success("Data Science insights loaded successfully.")
