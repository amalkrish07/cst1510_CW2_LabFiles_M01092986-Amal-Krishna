import pandas as pd
from pathlib import Path
from app.data.db import connect_database, DB_PATH
from app.services.user_service import register_user, login_user, migrate_users_from_file
from app.data.incidents import (
    insert_incident,
    update_incident_status,
    delete_incident,
    get_all_incidents,
    get_incidents_by_type_count,
    get_high_severity_by_status
)
from app.data.datasets import (
    insert_dataset,
    get_all_datasets,
    update_dataset,
    delete_dataset,
    count_datasets_by_category
)
from app.data.tickets import (
    insert_ticket,
    get_all_tickets,
    update_ticket,
    delete_ticket,
    count_tickets_by_priority
)
from app.services.setup_service import setup_database_complete
from app.services.load_csv import load_all_csv_data

if __name__ == "__main__":
    setup_database_complete()

    conn = connect_database()

    success, msg = register_user("alice", "SecurePass123!", "analyst")
    print(msg)

    success, msg = login_user("alice", "SecurePass123!")
    print(msg)

    incident_id = insert_incident(
        conn,
        "2024-11-05",
        "Phishing",
        "High",
        "Open",
        "Suspicious email detected",
        "alice"
    )
    print(f"Created incident #{incident_id}")

    df_incidents = get_all_incidents(conn)
    print(f"Total incidents: {len(df_incidents)}")

    dataset_id = insert_dataset(
        conn,
        "Network Logs Nov",
        "Network Logs",
        "Internal",
        "2024-11-10",
        5000,
        12.5
    )
    print(f"Created dataset #{dataset_id}")

    df_datasets = get_all_datasets(conn)
    print(f"Total datasets: {len(df_datasets)}")

    ticket_id = insert_ticket(
        conn,
        "TCK-1001",
        "High",
        "Open",
        "Network",
        "Router outage",
        "Main office router down",
        "2024-11-05"
    )
    print(f"Created ticket #{ticket_id}")

    df_tickets = get_all_tickets(conn)
    print(f"Total tickets: {len(df_tickets)}")

    df_by_type = get_incidents_by_type_count(conn)
    print("\nIncidents by Type:")
    print(df_by_type)

    df_high = get_high_severity_by_status(conn)
    print("\nHigh Severity Incidents by Status:")
    print(df_high)

    df_datasets_count = count_datasets_by_category(conn)
    print("\nDatasets by Category:")
    print(df_datasets_count)

    df_tickets_count = count_tickets_by_priority(conn)
    print("\nTickets by Priority:")
    print(df_tickets_count)

    conn.close()
