import os
import bcrypt
import re

USER_DATA_FILE = "users.txt"

def hash_password(plain_text_password):
    password_bytes = plain_text_password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)

    return hashed.decode('utf-8')

def verify_password(plain_text_password, hashed_password):
    password_bytes = plain_text_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')

    return bcrypt.checkpw(password_bytes, hashed_bytes)

def register_user(username, password, filename="users.txt"):
    if not os.path.exists(filename):
        open(filename, "w").close()

    with open(filename, "r") as f:
        for line in f:
            stored_username = line.strip().split(",")[0]
            if username == stored_username:
                return False

    hashed = hash_password(password)

    with open(filename, "a") as f:
        f.write(f"{username},{hashed}\n")

    return True

def user_exists(username):
    if not os.path.exists(USER_DATA_FILE):
        return False

    with open(USER_DATA_FILE, "r") as f:
        for line in f:
            stored_username = line.strip().split(",")[0]
            if username == stored_username:
                return True
    return False

def login_user(username, password):
    if not os.path.exists(USER_DATA_FILE):
        return False

    with open(USER_DATA_FILE, "r") as f:
        for line in f:
            stored_username, stored_hash = line.strip().split(",", 1)
            if username == stored_username:
                return verify_password(password, stored_hash)

    return False

def validate_username(username):
    if not username:
        return False, "Username cannot be empty"
    if " " in username:
        return False, "Username cannot contain spaces"
    if not re.match("^[A-Za-z0-9_]+$", username):
        return False, "Username can only contain letters, numbers, and underscores"
    return True, ""

def validate_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one number"
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character"
    return True, ""
