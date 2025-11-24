import bcrypt
from pathlib import Path
from app.data.db import connect_database
from app.data.users import get_user_by_username, insert_user
from app.data.schema import create_users_table

def register_user(username, password, role='user'):
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
        return True, f"Login successful!"
    return False, "Incorrect password."

def migrate_users_from_file(filepath='DATA/users.txt'):
    filepath = Path(filepath)
    if not filepath.exists():
        return False, f"User file not found at {filepath}"
    conn = connect_database()
    create_users_table(conn)
    conn.close()

    migrated = 0
    skipped = 0

    with filepath.open("r") as file:
        for line in file:
            line = line.strip()
            if not line or ":" not in line:
                continue

            username, password = line.split(":", 1)
            username, password = username.strip(), password.strip()

            existing_user = get_user_by_username(username)
            if existing_user:
                skipped += 1
                continue

            password_hash = bcrypt.hashpw(
                password.encode('utf-8'),
                bcrypt.gensalt()
            ).decode('utf-8')

            insert_user(username, password_hash)
            migrated += 1

    return True, f"Migrated {migrated} users, skipped {skipped} existing users."
