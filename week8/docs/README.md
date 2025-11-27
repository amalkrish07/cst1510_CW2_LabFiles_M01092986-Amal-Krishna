# Week 8: Data Pipeline & CRUD (SQL)

**Student Name:** Amal Krishna Mangalappilly Udhayakumar
**Student ID:** M01092986
**Course:** BSc Information Technology

## Project Description

A command-line database system implementing a full data pipeline with CRUD operations.
This system allows users to register securely, log in, manage cyber incidents, datasets, and IT tickets, and perform analytical queries on stored data.

## Features

- **User Management**

  - Register users with hashed passwords using bcrypt
  - User login with password verification
  - Duplicate username prevention
  - Role assignment (`user`, `admin`, `analyst`)
  - Migrate users from `users.txt` to database

- **Cyber Incident Management**

  - Create, read, update, and delete incidents
  - Track incident type, severity, status, description, and reporter
  - Analytical queries:
    - Count incidents by type
    - Count high-severity incidents by status
    - Identify incident types with more than a specified number of cases

- **Dataset Management**

  - Load dataset metadata from CSV files
  - Track dataset name, category, source, last update, record count, and file size
  - Query datasets by category

- **IT Ticket Management**

  - CRUD operations on IT tickets
  - Track ticket ID, priority, status, category, subject, description, and assignment
  - Generate reports by priority

- **Database Setup**

  - Automated database setup function:
    1. Connect to SQLite database
    2. Create all tables (`users`, `cyber_incidents`, `datasets_metadata`, `it_tickets`)
    3. Migrate users from `users.txt`
    4. Load CSV data for incidents, datasets, and tickets
    5. Verify database setup and display row counts

- **Testing**
  - Comprehensive tests for authentication, CRUD operations, and analytical queries

## Technical Implementation

- **Database:** SQLite
- **Data Pipeline:** Pandas for CSV reading and bulk loading (`to_sql`)
- **Password Security:** bcrypt hashing with automatic salting
- **Tables:**
  - `users` — stores username, password hash, role
  - `cyber_incidents` — stores incident details
  - `datasets_metadata` — stores dataset details
  - `it_tickets` — stores IT ticket details
- **CSV Files:**
  - `DATA/users.txt` — initial user credentials
  - `DATA/incidents.csv` — incident data
  - `DATA/datasets.csv` — dataset metadata
  - `DATA/tickets.csv` — IT tickets
