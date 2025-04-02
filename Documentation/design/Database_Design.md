# Database Design Document

## Face Recognition Attendance System

### Table of Contents

- [Database Design Document](#database-design-document)
  - [Face Recognition Attendance System](#face-recognition-attendance-system)
    - [Table of Contents](#table-of-contents)
  - [1. Introduction](#1-introduction)
  - [2. Database Management System](#2-database-management-system)
  - [3. Entity-Relationship Diagram](#3-entity-relationship-diagram)
  - [4. Database Schema](#4-database-schema)
    - [4.1 Users Table](#41-users-table)
    - [4.2 Attendance Table](#42-attendance-table)
  - [5. Database Optimization](#5-database-optimization)
    - [5.1 Indexes](#51-indexes)
    - [5.2 Constraints](#52-constraints)
    - [5.3 Triggers](#53-triggers)
  - [6. Data Access Layer](#6-data-access-layer)
  - [7. Query Examples](#7-query-examples)
  - [8. Data Integrity](#8-data-integrity)
  - [9. Backup and Recovery](#9-backup-and-recovery)

## 1. Introduction

This document describes the database design for the Face Recognition Attendance System. The database stores user profiles, facial recognition data, and attendance records. The design focuses on efficiency, data integrity, and ease of access for reporting and analytics.

## 2. Database Management System

The system uses SQLite as its database management system due to its:

- Serverless architecture (no separate server process required)
- Zero-configuration setup
- Cross-platform compatibility
- Self-contained design (entire database in a single file)
- Reliability for desktop applications

SQLite is ideal for this standalone application where concurrent access is not a requirement and the database size remains manageable.

## 3. Entity-Relationship Diagram

```txt
┌────────────────┐        ┌──────────────────┐
│    Users       │        │   Attendance     │
├────────────────┤        ├──────────────────┤
│ id (PK)        │        │ attendance_id(PK)│
│ name           │◄───────┤ id (FK)          │
│ enrollment_date│        │ name             │
│ last_updated   │        │ date             │
│ active         │        │ time             │
└────────────────┘        │ timestamp        │
                          └──────────────────┘
```

Relationship descriptions:

- One user can have multiple attendance records (one-to-many relationship)
- Each attendance record belongs to exactly one user
- The relationship is enforced through a foreign key constraint with cascade delete

## 4. Database Schema

### 4.1 Users Table

The Users table stores information about registered individuals in the system.

```sql
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    enrollment_date TEXT DEFAULT (datetime('now', 'localtime')),
    last_updated TEXT DEFAULT (datetime('now', 'localtime')),
    active INTEGER DEFAULT 1 NOT NULL CHECK (active IN (0, 1))
)
```

**Fields:**

- **id**: Unique identifier for the user (primary key)
  - Format: Custom format defined by the application
  - Example: "User.1", "User.2"
  
- **name**: Full name of the user
  - Not nullable to ensure every user has a name
  - Used for display and identification purposes
  
- **enrollment_date**: Date when the user was registered
  - Default value: Current date and time
  - Format: SQLite datetime format in local timezone
  - Example: "2025-04-02 15:30:45"
  
- **last_updated**: Timestamp of the last update to the user record
  - Default value: Current date and time
  - Updated automatically via trigger when record is modified
  - Format: SQLite datetime format in local timezone
  
- **active**: Boolean flag indicating if the user is active
  - 1 = Active (default)
  - 0 = Inactive (deactivated)
  - Used to soft-delete users without removing data
  - Constraint ensures only values 0 or 1 are accepted

### 4.2 Attendance Table

The Attendance table records attendance entries for users recognized by the system.

```sql
CREATE TABLE IF NOT EXISTS attendance (
    attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    id TEXT NOT NULL,
    name TEXT NOT NULL,
    date TEXT NOT NULL,
    time TEXT NOT NULL,
    timestamp INTEGER DEFAULT (strftime('%s','now')),
    FOREIGN KEY (id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE(id, date)
)
```

**Fields:**

- **attendance_id**: Unique identifier for the attendance record (primary key)
  - Auto-incrementing integer
  - System-generated
  
- **id**: Foreign key referencing the user's ID
  - Not nullable to ensure every attendance record is associated with a user
  - Linked to users table
  
- **name**: Name of the user
  - Denormalized from users table for reporting efficiency
  - Not nullable to ensure data completeness
  
- **date**: Date when attendance was recorded
  - Format: YYYY-MM-DD
  - Not nullable to ensure data validity
  - Part of unique constraint to prevent duplicate daily entries
  
- **time**: Time when attendance was recorded
  - Format: HH:MM:SS
  - Not nullable to ensure data validity
  
- **timestamp**: Unix timestamp for sorting and calculations
  - System-generated at insertion time
  - Used for efficient date-based filtering and calculations

## 5. Database Optimization

### 5.1 Indexes

The database uses the following indexes to optimize query performance:

```sql
CREATE INDEX IF NOT EXISTS idx_attendance_date ON attendance(date)
CREATE INDEX IF NOT EXISTS idx_attendance_id ON attendance(id)
CREATE INDEX IF NOT EXISTS idx_attendance_timestamp ON attendance(timestamp)
CREATE INDEX IF NOT EXISTS idx_users_active ON users(active)
CREATE INDEX IF NOT EXISTS idx_users_name ON users(name)
```

**Performance Implications:**

- **idx_attendance_date**: Speeds up queries filtering by date for daily reports
- **idx_attendance_id**: Optimizes lookups of attendance records by user ID
- **idx_attendance_timestamp**: Improves performance for time-range queries
- **idx_users_active**: Accelerates filtering of active vs. inactive users
- **idx_users_name**: Optimizes searches and sorting by name

### 5.2 Constraints

The database includes the following constraints for data integrity:

- **Primary Key Constraints**:
  - `id` in the users table
  - `attendance_id` in the attendance table

- **Foreign Key Constraints**:
  - `id` in attendance references `id` in users with cascade delete
    - If a user is deleted, all related attendance records will be deleted

- **Unique Constraints**:
  - `(id, date)` combination in attendance table
    - Prevents duplicate attendance for the same user on the same day

- **Check Constraints**:
  - `active IN (0, 1)` in users table
    - Ensures the active field can only be 0 or 1

- **Not Null Constraints**:
  - Applied to critical fields to ensure data completeness

### 5.3 Triggers

The database employs the following trigger to automatically maintain data:

```sql
CREATE TRIGGER IF NOT EXISTS update_user_timestamp 
AFTER UPDATE ON users
FOR EACH ROW
BEGIN
    UPDATE users SET last_updated = datetime('now', 'localtime') WHERE id = NEW.id;
END
```

**Purpose**:

- Automatically updates the `last_updated` field when a user record is modified
- Ensures accurate tracking of when records were last changed
- Reduces the need for application code to handle this common task

## 6. Data Access Layer

The database interaction is encapsulated in the `db_manager.py` module, which provides an abstraction layer between the application and the database. This module:

1. **Establishes database connections**
   - Creates and manages SQLite connection objects
   - Implements connection pooling if needed for performance
   - Handles connection errors gracefully

2. **Initializes the database schema**
   - Creates tables if they don't exist
   - Creates indexes for performance optimization
   - Sets up triggers for automated field updates

3. **Provides CRUD operations**
   - Functions for creating, reading, updating, and deleting records
   - Parameter sanitization to prevent SQL injection
   - Error handling and transaction management

4. **Implements domain-specific queries**
   - Functions for retrieving attendance by date, user, etc.
   - Methods for generating reports and statistics
   - Support for filtering and sorting results

## 7. Query Examples

The database design supports the following common queries:

**User Management:**

```sql
-- Get all users
SELECT id, name, enrollment_date, last_updated, active FROM users ORDER BY name

-- Get only active users
SELECT id, name, enrollment_date FROM users WHERE active = 1 ORDER BY name

-- Get user details by ID
SELECT name, enrollment_date, last_updated, active FROM users WHERE id=?

-- Deactivate a user
UPDATE users SET active = 0 WHERE id = ?

-- Reactivate a user
UPDATE users SET active = 1 WHERE id = ?
```

**Attendance Management:**

```sql
-- Record attendance
INSERT INTO attendance (id, name, date, time) VALUES (?, ?, ?, ?)

-- Check if attendance already recorded for a user on specific date
SELECT * FROM attendance WHERE id=? AND date=?

-- Get attendance records by date
SELECT a.id, u.name, a.time 
FROM attendance a 
JOIN users u ON a.id = u.id 
WHERE a.date=? 
ORDER BY a.time

-- Get attendance history for a specific user
SELECT date, time 
FROM attendance 
WHERE id=? 
ORDER BY date DESC, time DESC
```

**Statistics and Reporting:**

```sql
-- Get daily attendance counts
SELECT date, COUNT(*) as count 
FROM attendance 
GROUP BY date 
ORDER BY date DESC

-- Get monthly attendance summary
SELECT strftime('%Y-%m', date) as month, 
       COUNT(DISTINCT id) as unique_users, 
       COUNT(*) as total_records 
FROM attendance 
GROUP BY month 
ORDER BY month DESC

-- Get attendance frequency by user
SELECT u.name, COUNT(a.date) as days_present 
FROM users u 
LEFT JOIN attendance a ON u.id = a.id 
WHERE u.active = 1 
GROUP BY u.id 
ORDER BY days_present DESC
```

## 8. Data Integrity

The database design ensures data integrity through:

1. **Relational Integrity**
   - Foreign key constraints between users and attendance tables
   - Cascade delete to maintain referential integrity

2. **Domain Integrity**
   - Check constraints on the active field (0 or 1)
   - Automated date/time values for temporal fields
   - Not NULL constraints on required fields

3. **Entity Integrity**
   - Primary key constraints to ensure unique identification
   - Unique constraints to prevent duplicate attendance records

4. **Application-Level Validation**
   - Additional validation in the data access layer
   - Input sanitization to prevent SQL injection
   - Business logic checks before database operations

## 9. Backup and Recovery

The SQLite database file can be backed up using simple file-system operations:

1. **Backup Strategy**
   - Regular file copies of the database file
   - SQLite supports online backups while the database is in use
   - Application-level export/import functionality

2. **Recovery Process**
   - Replace corrupted database file with backup copy
   - Database integrity check functions
   - Transaction rollback for failed operations

3. **Database Maintenance**
   - Periodic VACUUM operations to reclaim space
   - Integrity checks to ensure database health
   - Index rebuilding for optimal performance
