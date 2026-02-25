Romanian version: [link](README.ro.md)

---

# Record Label Management System

This project implements a Django-based Record Label Management System designed to simulate and manage core activities of a music production platform, including artist administration, album management, track organization, user authentication, and structured message processing.

The application is developed in Python using Django and demonstrates a structured, modular approach to backend web development. Its primary goal is to showcase clean architecture, advanced form validation, database relationships, authentication mechanisms, and server-side data processing.

---

## System Overview

The platform allows users to:

- Browse and filter artists
- View albums and track listings
- Sort and paginate results dynamically
- Register and authenticate users
- Submit validated contact messages
- Store structured JSON message data
- Manage content through Django Admin

---

## Technical Highlights

### Custom User Model
The system extends Django’s `AbstractUser` to include additional profile fields such as:
- Date of birth
- Phone number
- Address
- City
- County
- Postal code

### Advanced Form Validation
The application implements complex validation logic including:
- Age validation (18+)
- Romanian CNP validation
- Word count and formatting constraints
- Forbidden email domain filtering
- Signature verification in contact messages
- Custom validation across multiple fields

### Data Relationships
The database structure includes:
- Genres
- Artists
- Albums
- Tracks

Implemented using Django ORM with proper ForeignKey relationships and related_name usage.

### Pagination and Filtering
Artist listing supports:
- Filtering by name
- Filtering by genre
- Filtering by formation year range
- Adjustable page size
- Alphabetical sorting (A–Z / Z–A)

### Middleware Integration
Custom middleware processes requests and modifies response headers.

### JSON Data Processing
Contact messages are:
- Preprocessed
- Validated
- Structured
- Saved as JSON files
- Tagged as urgent based on business rules
- Stored with metadata (IP address, timestamp)

---

## Technologies Used

- Python
- Django
- SQLite
- Django ORM
- HTML Templates
- Custom Validators
- Custom Middleware

---

## Architectural Principles

The project emphasizes:

- Clear separation of responsibilities
- Server-side validation
- Modular structure
- Maintainable and readable code
- Proper use of Django’s ecosystem
- Structured data processing

---

## Academic Context

Developed as part of second-year coursework in Computer Science (University of Bucharest).

The project demonstrates applied knowledge of:

- Object-oriented programming
- Web backend development
- Data validation
- Relational databases
- Authentication systems
