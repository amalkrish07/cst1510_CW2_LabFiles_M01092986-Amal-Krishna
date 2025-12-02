# Week 9: Cyber Intelligence Platform

**Student Name:** Amal Krishna Mangalappilly Udhayakumar
**Student ID:** M01092986
**Course:** BSc Information Technology

## Project Description

A Streamlit-based web application for managing cybersecurity incidents, IT tickets, and datasets. Users can register, log in, and view domain-specific dashboards with metrics and visualizations. CRUD operations are supported for all data types.

## Features

### Authentication

- User registration with secure password hashing (bcrypt)
- Login/logout with session management
- Role-based access control (`user`, `admin`, `analyst`)

### Dashboard & Analytics

- Domain-specific metrics (Cybersecurity, Data Science, IT Operations)
- Visualizations with bar and line charts
- Summary metrics with `st.metric()`

### CRUD Operations

- Incidents: create, read, update, delete
- Tickets: create, read, update, delete
- Datasets metadata: manage records efficiently

### Pages

- **Home:** Login/Register
- **Dashboard:** Summary metrics and tables
- **Analytics:** Domain insights with charts
- **Incidents:** Manage incident records
- **Tickets:** Manage IT tickets
- **Datasets:** Manage datasets metadata
- **Settings:** User account management

### Database

- SQLite database (`intelligence_platform.db`) stored in `week8/app/DATA/`
- Tables: `users`, `cyber_incidents`, `it_tickets`, `datasets_metadata`
