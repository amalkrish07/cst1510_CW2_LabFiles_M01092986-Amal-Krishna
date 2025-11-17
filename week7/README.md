# Week 7: Secure Authentication System

**Student Name:** Amal Krishna Mangalappilly Udhayakumar
**Student ID:** M01092986
**Course:** BSc Information Technology

## Project Description

A command-line authentication system implementing secure password hashing.
This system allows users to register accounts and log in with proper password verification.

## Features

- Secure password hashing using bcrypt with automatic salt generation
- User registration with duplicate username prevention
- User login with password verification
- Input validation for usernames and passwords
- File-based user data persistence

## Technical Implementation

- **Hashing Algorithm:** bcrypt with automatic salting
- **Data Storage:** Plain text file (`users.txt`) with comma-separated values
- **Password Security:** One-way hashing, no plaintext storage
- **Validation:**
  - Username: 3-20 alphanumeric characters (letters, numbers, underscores)
  - Password: 6-50 characters with at least one uppercase letter, one lowercase letter, one number, and one special character
