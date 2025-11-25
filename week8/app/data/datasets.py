import pandas as pd
from app.data.db import connect_database

def insert_dataset(conn, dataset_name, category, source, last_updated, record_count, file_size_mb):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO datasets_metadata (dataset_name, category, source, last_updated, record_count, file_size_mb) VALUES (?, ?, ?, ?, ?, ?)",
        (dataset_name, category, source, last_updated, record_count, file_size_mb)
    )
    conn.commit()
    return cursor.lastrowid

def get_all_datasets(conn):
    df = pd.read_sql_query("SELECT * FROM datasets_metadata ORDER BY id DESC", conn)
    return df

def update_dataset(conn, dataset_id, **kwargs):
    fields = ", ".join(f"{k} = ?" for k in kwargs.keys())
    values = list(kwargs.values())
    values.append(dataset_id)
    cursor = conn.cursor()
    cursor.execute(f"UPDATE datasets_metadata SET {fields} WHERE id = ?", values)
    conn.commit()
    return cursor.rowcount

def delete_dataset(conn, dataset_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM datasets_metadata WHERE id = ?", (dataset_id,))
    conn.commit()
    return cursor.rowcount

def count_datasets_by_category(conn):
    query = "SELECT category, COUNT(*) as count FROM datasets_metadata GROUP BY category ORDER BY count DESC"
    df = pd.read_sql_query(query, conn)
    return df
