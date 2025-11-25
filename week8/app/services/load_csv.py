import pandas as pd
from pathlib import Path
from app.data.db import connect_database

def load_csv_to_table(conn, csv_path, table_name):
    csv_path = Path(csv_path)
    if not csv_path.exists():
        return 0
    df = pd.read_csv(csv_path)
    df.to_sql(name=table_name, con=conn, if_exists='append', index=False)
    return len(df)

def load_all_csv_data(conn):
    total_rows = 0
    total_rows += load_csv_to_table(conn, 'DATA/cyber_incidents.csv', 'cyber_incidents')
    total_rows += load_csv_to_table(conn, 'DATA/datasets_metadata.csv', 'datasets_metadata')
    total_rows += load_csv_to_table(conn, 'DATA/it_tickets.csv', 'it_tickets')
    return total_rows
