import pandas as pd

def insert_ticket(conn, ticket_id, priority, status, category, subject, description, created_date, resolved_date=None, assigned_to=None):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO it_tickets (ticket_id, priority, status, category, subject, description, created_date, resolved_date, assigned_to) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (ticket_id, priority, status, category, subject, description, created_date, resolved_date, assigned_to)
    )
    conn.commit()
    return cursor.lastrowid

def get_all_tickets(conn):
    df = pd.read_sql_query("SELECT * FROM it_tickets ORDER BY id DESC", conn)
    return df

def update_ticket(conn, ticket_id, **kwargs):
    fields = ", ".join(f"{k} = ?" for k in kwargs.keys())
    values = list(kwargs.values())
    values.append(ticket_id)
    cursor = conn.cursor()
    cursor.execute(f"UPDATE it_tickets SET {fields} WHERE ticket_id = ?", values)
    conn.commit()
    return cursor.rowcount

def delete_ticket(conn, ticket_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM it_tickets WHERE ticket_id = ?", (ticket_id,))
    conn.commit()
    return cursor.rowcount

def count_tickets_by_priority(conn):
    query = "SELECT priority, COUNT(*) as count FROM it_tickets GROUP BY priority ORDER BY count DESC"
    df = pd.read_sql_query(query, conn)
    return df
