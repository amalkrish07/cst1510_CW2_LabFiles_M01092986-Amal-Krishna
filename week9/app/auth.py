import os
import bcrypt
import re
import time
import secrets

FAILED_ATTEMPTS_FILE = "data/failed_attempts.txt"
LOCKOUT_DURATION = 5 * 60
MAX_ATTEMPTS = 3
SESSIONS_FILE = "data/sessions.txt"
USER_DATA_FILE = "data/users.txt"

def create_session(username):
    token = secrets.token_hex(16)
    timestamp = time.time()
    with open(SESSIONS_FILE, "a") as f:
        f.write(f"{username},{token},{timestamp}\n")
    return token

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

def validate_username(username):
    if len(username) < 3 or len(username) > 20:
        return False, "Username must be 3–20 characters long"
    if " " in username:
        return False, "Username cannot contain spaces"
    if not re.match("^[A-Za-z0-9_]+$", username):
        return False, "Only letters, numbers, and underscores allowed"
    return True, ""

def validate_password(password):
    if len(password) < 6 or len(password) > 50:
        return False, "Password must be 6–50 characters long"
    if not re.search(r"[A-Z]", password):
        return False, "Must contain at least one uppercase letter"
    if not re.search(r"[a-z]", password):
        return False, "Must contain at least one lowercase letter"
    if not re.search(r"[0-9]", password):
        return False, "Must contain at least one number"
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Must contain at least one special character"
    return True, ""

def check_password_strength(password):
    score = 0
    if len(password) >= 8: score += 1
    if re.search(r"[A-Z]", password): score += 1
    if re.search(r"[a-z]", password): score += 1
    if re.search(r"[0-9]", password): score += 1
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password): score += 1

    if score <= 2:
        return "Weak"
    elif score <= 4:
        return "Medium"
    else:
        return "Strong"

def register_new_user(username, password, role):
    is_valid, msg = validate_username(username)
    if not is_valid:
        return False, msg

    is_valid, msg = validate_password(password)
    if not is_valid:
        return False, msg

    if not os.path.exists(USER_DATA_FILE):
        open(USER_DATA_FILE, "w").close()

    with open(USER_DATA_FILE, "r") as f:
        for line in f:
            stored_username = line.strip().split(",")[0]
            if username == stored_username:
                return False, "Username already exists."

    hashed = hash_password(password)
    with open(USER_DATA_FILE, "a") as f:
        f.write(f"{username},{hashed},{role}\n")

    return True, f"User registered successfully with role: {role}"

def load_failed_attempts():
    attempts = {}
    if os.path.exists(FAILED_ATTEMPTS_FILE):
        with open(FAILED_ATTEMPTS_FILE, "r") as f:
            for line in f:
                username, count, timestamp = line.strip().split(",")
                attempts[username] = (int(count), float(timestamp))
    return attempts


def save_failed_attempts(attempts):
    with open(FAILED_ATTEMPTS_FILE, "w") as f:
        for username, (count, timestamp) in attempts.items():
            f.write(f"{username},{count},{timestamp}\n")

def login_user(username, password):
    attempts = load_failed_attempts()

    if username in attempts:
        count, last_time = attempts[username]

        if count >= MAX_ATTEMPTS and time.time() - last_time < LOCKOUT_DURATION:
            return False, None, "Account locked. Try again later."

        elif time.time() - last_time >= LOCKOUT_DURATION:
            attempts[username] = (0, 0)
            save_failed_attempts(attempts)

    if not os.path.exists(USER_DATA_FILE):
        return False, None, "User database not found."

    with open(USER_DATA_FILE, "r") as f:
        for line in f:
            stored_username, stored_hash, role = line.strip().split(",", 2)

            if username == stored_username:

                if verify_password(password, stored_hash):
                    attempts[username] = (0, 0)
                    save_failed_attempts(attempts)
                    token = create_session(username)
                    return True, role, token

                count, _ = attempts.get(username, (0, 0))
                attempts[username] = (count + 1, time.time())
                save_failed_attempts(attempts)

                return False, None, f"Incorrect password. Attempt {attempts[username][0]}/{MAX_ATTEMPTS}"

    return False, None, "User not found."
