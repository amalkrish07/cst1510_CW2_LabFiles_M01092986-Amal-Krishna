import bcrypt
from week8.app.data.db import connect_database

def get_user_by_username(username):
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, username, password_hash, role FROM users WHERE username = ?",
        (username,)
    )
    user = cursor.fetchone()
    conn.close()
    return user


def insert_user(username, plain_password, role='user'):
    conn = connect_database()
    cursor = conn.cursor()

    # Hashing password using bcrypt
    password_bytes = plain_password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt).decode("utf-8")

    cursor.execute(
        "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
        (username, hashed, role)
    )
    conn.commit()
    conn.close()


def verify_password(plain_password, stored_hash):
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        stored_hash.encode("utf-8")
    )
