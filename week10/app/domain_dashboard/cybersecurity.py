import streamlit as st
from app.db_files.db import connect_database
from app.db_files import incidents
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

system_prompt = """You are a cybersecurity expert assistant.
Analyze incidents, threats, and provide technical guidance."""

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

    if "cyber_messages" not in st.session_state:
        st.session_state.cyber_messages = []

    with st.sidebar:
        st.header("Cybersecurity AI Assistant")

        if st.button("Clear Chat"):
            st.session_state.cyber_messages = []

        user_input = st.text_input("Ask AI about incidents or threats:")

        if st.button("Send"):
            if user_input:
                st.session_state.cyber_messages.append({"role": "user", "content": user_input})
                response = client.chat.completions.create(
                    model="gpt-4.1-mini",
                    messages=[{"role": "system", "content": system_prompt}, *st.session_state.cyber_messages]
                )
                reply = response.choices[0].message.content
                st.session_state.cyber_messages.append({"role": "assistant", "content": reply})

        for msg in st.session_state.cyber_messages:
            if msg["role"] == "user":
                st.markdown(f"**You:** {msg['content']}")
            else:
                st.markdown(f"**AI:** {msg['content']}")

    st.success("Cybersecurity insights loaded successfully.")
