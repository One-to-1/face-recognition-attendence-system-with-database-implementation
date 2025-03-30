"""
Database schema for the Face Recognition Attendance System.

This file defines the structure of the database used in the application.
The tables are created in the DatabaseManager class based on these schema definitions.
"""

# Database file path is defined in config/settings.py (DB_PATH)

# Users table schema - improved with better constraints and additional fields
USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    enrollment_date TEXT DEFAULT (datetime('now', 'localtime')),
    last_updated TEXT DEFAULT (datetime('now', 'localtime')),
    active INTEGER DEFAULT 1 NOT NULL CHECK (active IN (0, 1))
)
"""

# Attendance table schema - improved with timestamp and unique constraints
ATTENDANCE_TABLE = """
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
"""

# Indexes for performance optimization
INDEXES = [
    "CREATE INDEX IF NOT EXISTS idx_attendance_date ON attendance(date)",
    "CREATE INDEX IF NOT EXISTS idx_attendance_id ON attendance(id)",
    "CREATE INDEX IF NOT EXISTS idx_attendance_timestamp ON attendance(timestamp)",
    "CREATE INDEX IF NOT EXISTS idx_users_active ON users(active)",
    "CREATE INDEX IF NOT EXISTS idx_users_name ON users(name)"
]

# Triggers to automatically update the last_updated field
TRIGGERS = [
    """
    CREATE TRIGGER IF NOT EXISTS update_user_timestamp 
    AFTER UPDATE ON users
    FOR EACH ROW
    BEGIN
        UPDATE users SET last_updated = datetime('now', 'localtime') WHERE id = NEW.id;
    END
    """
]

# Sample queries
QUERY_EXAMPLES = {
    # User management
    "get_all_users": "SELECT id, name, enrollment_date, last_updated, active FROM users ORDER BY name",
    "get_active_users": "SELECT id, name, enrollment_date FROM users WHERE active = 1 ORDER BY name",
    "get_user_by_id": "SELECT name, enrollment_date, last_updated, active FROM users WHERE id=?",
    "deactivate_user": "UPDATE users SET active = 0 WHERE id = ?",
    "reactivate_user": "UPDATE users SET active = 1 WHERE id = ?",
    
    # Attendance management
    "record_attendance": "INSERT INTO attendance (id, name, date, time) VALUES (?, ?, ?, ?)",
    "check_attendance": "SELECT * FROM attendance WHERE id=? AND date=?",
    "get_attendance_by_date": "SELECT a.id, u.name, a.time FROM attendance a JOIN users u ON a.id = u.id WHERE a.date=? ORDER BY a.time",
    "get_attendance_by_user": "SELECT date, time FROM attendance WHERE id=? ORDER BY date DESC, time DESC",
    
    # Statistics and reporting
    "get_daily_attendance_count": "SELECT date, COUNT(*) as count FROM attendance GROUP BY date ORDER BY date DESC",
    "get_monthly_attendance": "SELECT strftime('%Y-%m', date) as month, COUNT(DISTINCT id) as unique_users, COUNT(*) as total_records FROM attendance GROUP BY month ORDER BY month DESC",
    "get_user_attendance_frequency": "SELECT u.name, COUNT(a.date) as days_present FROM users u LEFT JOIN attendance a ON u.id = a.id WHERE u.active = 1 GROUP BY u.id ORDER BY days_present DESC"
}