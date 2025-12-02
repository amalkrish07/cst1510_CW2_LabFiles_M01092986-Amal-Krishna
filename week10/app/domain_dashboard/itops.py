import streamlit as st
import pandas as pd
from app.db_files.db import connect_database
from app.db_files import incidents, tickets
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

system_prompt = """You are an IT operations expert assistant.
Help troubleshoot issues, optimize systems, and manage tickets."""

def show_dashboard(st):
    conn = connect_database()
    st.title("🖥️ IT Operations Dashboard")

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

    if "it_messages" not in st.session_state:
        st.session_state.it_messages = []

    with st.sidebar:
        st.header("IT Ops AI Assistant")

        if st.button("Clear Chat"):
            st.session_state.it_messages = []

        user_input = st.text_input("Ask AI about IT issues or tickets:")

        if st.button("Send"):
            if user_input:
                st.session_state.it_messages.append({"role": "user", "content": user_input})
                response = client.chat.completions.create(
                    model="gpt-4.1-mini",
                    messages=[{"role": "system", "content": system_prompt}, *st.session_state.it_messages]
                )
                reply = response.choices[0].message.content
                st.session_state.it_messages.append({"role": "assistant", "content": reply})

        for msg in st.session_state.it_messages:
            if msg["role"] == "user":
                st.markdown(f"**You:** {msg['content']}")
            else:
                st.markdown(f"**AI:** {msg['content']}")

    st.success("IT Operations insights loaded successfully.")
