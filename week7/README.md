# Week 7: Secure Authentication System

**Student Name:** Amal Krishna Mangalappilly Udhayakumar
**Student ID:** M01092986
**Course:** BSc Information Technology

## Project Description

A command-line authentication system implementing secure password hashing.
This system allows users to register accounts with specific roles, log in securely, and manage sessions.

## Features

- Secure password hashing using bcrypt with automatic salt generation
- User registration with duplicate username prevention and role assignment (`user`, `admin`, `analyst`)
- User login with password verification
- Password strength indicator (Weak / Medium / Strong)
- Input validation for usernames and passwords
- Account lockout after 3 failed login attempts (5-minute lock)
- Session management with unique session tokens
- File-based user data persistence (`users.txt`) and session tracking (`sessions.txt`)

## Technical Implementation

- **Hashing Algorithm:** bcrypt with automatic salting
- **Data Storage:** Plain text files:
  - `users.txt` — stores `username,hashed_password,role`
  - `sessions.txt` — stores active session tokens with timestamps
  - `failed_attempts.txt` — tracks failed login attempts for lockout
- **Password Security:** One-way hashing, no plaintext storage
- **Validation:**
  - Username: 3-20 alphanumeric characters (letters, numbers, underscores)
  - Password: 6-50 characters with at least one uppercase letter, one lowercase letter, one number, and one special character
