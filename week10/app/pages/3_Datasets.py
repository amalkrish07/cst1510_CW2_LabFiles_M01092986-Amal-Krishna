import streamlit as st
import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db_files.db import connect_database
from app.db_files import schema

st.set_page_config(page_title="Datasets", page_icon="📂", layout="wide")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must log in to access the Datasets page.")
    st.stop()

st.title("📂 Datasets Metadata")

conn = connect_database()

schema.create_datasets_metadata_table(conn)

with st.expander("➕ Add New Dataset"):
    st.subheader("Add New Dataset")
    with st.form("dataset_form", clear_on_submit=True):
        dataset_name = st.text_input("Dataset Name")
        category = st.text_input("Category")
        source = st.text_input("Source")
        last_updated = st.date_input("Last Updated")
        record_count = st.number_input("Record Count", min_value=0)
        file_size_mb = st.number_input("File Size (MB)", min_value=0.0, format="%.2f")

        submitted = st.form_submit_button("Add Dataset")
        if submitted:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO datasets_metadata
                (dataset_name, category, source, last_updated, record_count, file_size_mb)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (dataset_name, category, source, str(last_updated), record_count, file_size_mb)
            )
            conn.commit()
            st.success(f"Dataset '{dataset_name}' added successfully!")

st.subheader("All Datasets")
df_datasets = pd.read_sql_query("SELECT * FROM datasets_metadata ORDER BY id DESC", conn)
st.dataframe(df_datasets)

with st.expander("✏️ Update Dataset"):
    st.subheader("Update Dataset Info")
    update_id = st.number_input("Dataset ID", min_value=1, step=1)
    new_category = st.text_input("New Category")
    new_source = st.text_input("New Source")
    new_last_updated = st.date_input("New Last Updated")
    new_record_count = st.number_input("New Record Count", min_value=0)
    new_file_size_mb = st.number_input("New File Size (MB)", min_value=0.0, format="%.2f")

    if st.button("Update Dataset"):
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE datasets_metadata
            SET category = ?, source = ?, last_updated = ?, record_count = ?, file_size_mb = ?
            WHERE id = ?
            """,
            (new_category, new_source, str(new_last_updated), new_record_count, new_file_size_mb, update_id)
        )
        conn.commit()
        if cursor.rowcount:
            st.success(f"Dataset ID {update_id} updated successfully!")
        else:
            st.error("Dataset ID not found.")

with st.expander("🗑️ Delete Dataset"):
    st.subheader("Delete Dataset")
    delete_id = st.number_input("Dataset ID to Delete", min_value=1, step=1, key="delete_dataset_id")
    if st.button("Delete Dataset"):
        cursor = conn.cursor()
        cursor.execute("DELETE FROM datasets_metadata WHERE id = ?", (delete_id,))
        conn.commit()
        if cursor.rowcount:
            st.success(f"Dataset ID {delete_id} deleted successfully.")
        else:
            st.error("Dataset ID not found.")
