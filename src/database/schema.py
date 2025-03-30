"""
Database schema for the Face Recognition Attendance System.

This file documents the database structure but doesn't actually create it.
The tables are created in the DatabaseManager class.
"""

# Database file path is defined in config/settings.py (DB_PATH)

# Users table schema
USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL
)
"""

# Attendance table schema
ATTENDANCE_TABLE = """
CREATE TABLE IF NOT EXISTS attendance (
    id TEXT,
    name TEXT,
    date TEXT,
    time TEXT,
    FOREIGN KEY (id) REFERENCES users(id)
)
"""

# Indexes for performance
INDEXES = [
    "CREATE INDEX IF NOT EXISTS idx_attendance_date ON attendance(date)",
    "CREATE INDEX IF NOT EXISTS idx_attendance_id ON attendance(id)"
]

# Sample queries
QUERY_EXAMPLES = {
    "get_all_users": "SELECT id, name FROM users",
    "get_user_by_id": "SELECT name FROM users WHERE id=?",
    "record_attendance": "INSERT INTO attendance (id, name, date, time) VALUES (?, ?, ?, ?)",
    "check_attendance": "SELECT * FROM attendance WHERE id=? AND date=?",
    "get_attendance_by_date": "SELECT * FROM attendance WHERE date=?",
    "get_attendance_by_user": "SELECT * FROM attendance WHERE id=?"
}