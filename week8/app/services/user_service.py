import bcrypt
from pathlib import Path
from app.data.db import connect_database
from app.data.users import get_user_by_username, insert_user
from app.data.schema import create_users_table

BASE_DIR = Path(__file__).resolve().parent.parent.parent
USERS_FILE = BASE_DIR / "DATA" / "users.txt"

def register_user(username, password, role='user'):
    if get_user_by_username(username):
        return False, f"User '{username}' already exists."

    password_hash = bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')
    insert_user(username, password_hash, role)
    return True, f"User '{username}' registered successfully."


def login_user(username, password):
    user = get_user_by_username(username)
    if not user:
        return False, "User not found."
    stored_hash = user[2]
    if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
        return True, "Login successful!"
    return False, "Incorrect password."

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
