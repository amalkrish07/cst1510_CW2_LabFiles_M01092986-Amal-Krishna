import bcrypt
from pathlib import Path
from app.data.db import connect_database
from app.data.users import get_user_by_username, insert_user
from app.data.schema import create_users_table

BASE_DIR = Path(__file__).resolve().parent.parent.parent
USERS_FILE = BASE_DIR / "DATA" / "users.txt"

def register_user(username, password, role='user'):
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        conn.close()
        return False, f"Username '{username}' already exists."

    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    password_hash = hashed.decode('utf-8')

    cursor.execute(
        "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
        (username, password_hash, role)
    )
    conn.commit()
    conn.close()

    return True, f"User '{username}' registered successfully!"


def login_user(username, password):
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        return False, "Username not found."

    stored_hash = user[2]
    password_bytes = password.encode('utf-8')
    hash_bytes = stored_hash.encode('utf-8')

    if bcrypt.checkpw(password_bytes, hash_bytes):
        return True, f"Welcome, {username}!"
    else:
        return False, "Invalid password."

def migrate_users_from_file(filepath=USERS_FILE):
    if not filepath.exists():
        return False, f"User file not found at {filepath}"

    conn = connect_database()
    create_users_table(conn)
    cursor = conn.cursor()

    migrated = 0
    skipped = 0

    with filepath.open("r") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split(",")
            if len(parts) < 3:
                continue
            username, password_hash, role = map(str.strip, parts)
            try:
                cursor.execute(
                    "INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                    (username, password_hash, role)
                )
                if cursor.rowcount > 0:
                    migrated += 1
                else:
                    skipped += 1
            except Exception as e:
                print(f"Error migrating {username}: {e}")

    conn.commit()
    conn.close()
    return True, f"Migrated {migrated} users, skipped {skipped} existing users."
