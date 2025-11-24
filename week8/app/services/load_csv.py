import pandas as pd
from pathlib import Path

def load_csv_to_table(conn, csv_path, table_name):
    csv_path = Path(csv_path)
    if not csv_path.exists():
        print(f"File not found: {csv_path}")
        return 0

    df = pd.read_csv(csv_path)

    df.to_sql(name=table_name, con=conn, if_exists='append', index=False)

    row_count = len(df)
    print(f"Loaded {row_count} rows into '{table_name}' from {csv_path.name}")
    return row_count
