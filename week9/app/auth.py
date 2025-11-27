import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../week8')))

from app.data.db import connect_database
from app.data.users import insert_user, get_user_by_username

import bcrypt

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def login_user(username, password):
    user = get_user_by_username(username)
    if not user:
        return False, ""
    _, _, hashed_password, role = user
    if verify_password(password, hashed_password):
        return True, role
    return False, ""

def register_new_user(username, password, role="user"):
    if get_user_by_username(username):
        return False, "Username already exists"

    hashed = hash_password(password)
    insert_user(username, hashed, role)
    return True, "Account created successfully"
