# Database Schema Design

## Overview

This document details the database schema design for the Face Recognition Attendance System. The system uses SQLite for data persistence, with a carefully designed schema to support face recognition and attendance tracking operations.

## Entity-Relationship Diagram (ERD)

```txt
┌───────────────┐        ┌───────────────────────┐
│    USERS      │        │      ATTENDANCE        │
├───────────────┤        ├───────────────────────┤
│ id (PK)       │◄──────┤ attendance_id (PK)     │
│ name          │        │ id (FK)               │
│ enrollment_date│        │ name                  │
│ last_updated  │        │ date                  │
│ active        │        │ time                  │
└───────────────┘        │ timestamp             │
                         └───────────────────────┘
```

## Table Definitions

### Users Table

Stores information about registered students/users.

```sql
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    enrollment_date TEXT DEFAULT (datetime('now', 'localtime')),
    last_updated TEXT DEFAULT (datetime('now', 'localtime')),
    active INTEGER DEFAULT 1 NOT NULL CHECK (active IN (0, 1))
)
```

#### Fields

- **id**: Unique identifier for each user (typically student ID)
- **name**: Full name of the user
- **enrollment_date**: Date when the user was registered in the system
- **last_updated**: Last time the user record was modified
- **active**: Boolean flag (1=active, 0=inactive) to indicate if user is currently active

### Attendance Table

Records attendance events for registered users.

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

Fields

- **attendance_id**: Auto-incremented unique identifier for each attendance record
- **id**: Foreign key reference to users.id
- **name**: User's name (denormalized for faster queries)
- **date**: Date of attendance
- **time**: Time of attendance
- **timestamp**: Unix timestamp for faster range queries

## Database Indexes

Indexes are implemented to optimize query performance on frequently accessed fields:

```sql
CREATE INDEX IF NOT EXISTS idx_attendance_date ON attendance(date)
CREATE INDEX IF NOT EXISTS idx_attendance_id ON attendance(id)
CREATE INDEX IF NOT EXISTS idx_attendance_timestamp ON attendance(timestamp)
CREATE INDEX IF NOT EXISTS idx_users_active ON users(active)
CREATE INDEX IF NOT EXISTS idx_users_name ON users(name)
```

## Database Triggers

Automatically update the `last_updated` field when a user record is modified:

```sql
CREATE TRIGGER IF NOT EXISTS update_user_timestamp 
AFTER UPDATE ON users
FOR EACH ROW
BEGIN
    UPDATE users SET last_updated = datetime('now', 'localtime') WHERE id = NEW.id;
END
```

## Common Database Queries

### User Management Queries

1. **Get All Users**

   ```sql
   SELECT id, name, enrollment_date, last_updated, active 
   FROM users 
   ORDER BY name
   ```

2. **Get Active Users**

   ```sql
   SELECT id, name, enrollment_date 
   FROM users 
   WHERE active = 1 
   ORDER BY name
   ```

3. **Get User by ID**

   ```sql
   SELECT name, enrollment_date, last_updated, active 
   FROM users 
   WHERE id=?
   ```

4. **Deactivate User**

   ```sql
   UPDATE users 
   SET active = 0 
   WHERE id = ?
   ```

5. **Reactivate User**

   ```sql
   UPDATE users 
   SET active = 1 
   WHERE id = ?
   ```

### Attendance Management Queries

1. **Record Attendance**

   ```sql
   INSERT INTO attendance (id, name, date, time) 
   VALUES (?, ?, ?, ?)
   ```

2. **Check If Already Attended**

   ```sql
   SELECT * 
   FROM attendance 
   WHERE id=? AND date=?
   ```

3. **Get Attendance by Date**

   ```sql
   SELECT a.id, u.name, a.time 
   FROM attendance a 
   JOIN users u ON a.id = u.id 
   WHERE a.date=? 
   ORDER BY a.time
   ```

4. **Get User's Attendance History**

   ```sql
   SELECT date, time 
   FROM attendance 
   WHERE id=? 
   ORDER BY date DESC, time DESC
   ```

### Statistics and Reporting Queries

1. **Daily Attendance Count**

   ```sql
   SELECT date, COUNT(*) as count 
   FROM attendance 
   GROUP BY date 
   ORDER BY date DESC
   ```

2. **Monthly Attendance Summary**

   ```sql
   SELECT strftime('%Y-%m', date) as month, 
          COUNT(DISTINCT id) as unique_users, 
          COUNT(*) as total_records 
   FROM attendance 
   GROUP BY month 
   ORDER BY month DESC
   ```

3. **User Attendance Frequency**

   ```sql
   SELECT u.name, COUNT(a.date) as days_present 
   FROM users u 
   LEFT JOIN attendance a ON u.id = a.id 
   WHERE u.active = 1 
   GROUP BY u.id 
   ORDER BY days_present DESC
   ```

## Schema Design Considerations

1. **Denormalization**: User name is stored in both tables to reduce join operations for common queries
2. **Constraints**:
   - Users cannot be marked present twice on the same day (UNIQUE constraint)
   - Foreign key constraints ensure referential integrity
3. **Default Values**: System timestamps are used for enrollment dates and updates
4. **Indexes**: Carefully placed to accelerate common query patterns without excessive overhead

## Database Security Considerations

1. **Input Validation**: All user inputs are validated before database operations
2. **Parameterized Queries**: Used throughout the application to prevent SQL injection
3. **Minimal Permissions**: Database file permissions set to minimum required access

## Future Schema Evolution

1. **Course/Class Support**: Future versions may add tables for courses and class sessions
2. **Locations**: Support for multiple attendance locations
3. **Permissions**: Role-based permission system for administrative functions
