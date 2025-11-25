import pandas as pd
from pathlib import Path
from app.data.db import connect_database
from app.data.schema import create_all_tables
from app.services.user_service import migrate_users_from_file
from app.services.load_csv import load_all_csv_data
from app.data.db import DB_PATH


DB_PATH = Path("project_database.db")

def setup_database_complete():
    print("\n[1/5] Connecting to database...")
    conn = connect_database()
    print("Connected")

    print("\n[2/5] Creating database tables...")
    create_all_tables(conn)

    print("\n[3/5] Migrating users from users.txt...")
    user_count = migrate_users_from_file()
    print(f"Migrated {user_count} users")

    print("\n[4/5] Loading CSV data...")
    total_rows = load_all_csv_data(conn)

    print("\n[5/5] Verifying database setup...")
    cursor = conn.cursor()

    tables = ['users', 'cyber_incidents', 'datasets_metadata', 'it_tickets']
    print("\n Database Summary:")
    print(f"{'Table':<25} {'Row Count':<15}")

    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"{table:<25} {count:<15}")

    conn.close()
    print(f"\n Database location: {DB_PATH.resolve()}")
    print("\nYou're ready for Week 9 (Streamlit web interface)!")

setup_database_complete()
