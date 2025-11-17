import os
import bcrypt

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
