"""
Database manager for the Face Recognition Attendance System.
Handles all database operations including user registration and attendance recording.
"""

import sqlite3
from datetime import datetime
import os
import sys

# Add project root to path to allow imports from config
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from config.settings import DB_PATH

class DatabaseManager:
    def __init__(self):
        """Initialize database connection and create tables if they don't exist."""
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()

    def connect(self):
        """Connect to the SQLite database."""
        try:
            self.conn = sqlite3.connect(DB_PATH)
            self.cursor = self.conn.cursor()
            print(f"✅ Connected to database: {DB_PATH}")
        except sqlite3.Error as e:
            print(f"❌ Database connection error: {e}")
            raise

    def create_tables(self):
        """Create necessary tables if they don't exist."""
        try:
            # Users table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY UNIQUE,
                    name TEXT NOT NULL
                )
            """)
            
            # Attendance table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS attendance (
                    id TEXT,
                    name TEXT,
                    date TEXT,
                    time TEXT,
                    FOREIGN KEY (id) REFERENCES users(id)
                )
            """)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"❌ Error creating tables: {e}")
            raise

    def user_exists(self, user_id):
        """Check if a user ID already exists in the database.
        
        Args:
            user_id: The user ID to check
            
        Returns:
            bool: True if the user ID already exists, False otherwise
        """
        try:
            self.cursor.execute("SELECT id FROM users WHERE id=?", (user_id,))
            result = self.cursor.fetchone()
            return result is not None
        except sqlite3.Error as e:
            print(f"❌ Error checking if user exists: {e}")
            return False

    def register_user(self, user_id, name):
        """Register a new user or update existing user."""
        try:
            self.cursor.execute("INSERT OR REPLACE INTO users (id, name) VALUES (?, ?)", 
                               (user_id, name))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"❌ Error registering user: {e}")
            return False

    def record_attendance(self, user_id, name):
        """Record attendance for a user."""
        try:
            now = datetime.now()
            date = now.strftime("%Y-%m-%d")
            time = now.strftime("%H:%M:%S")
            
            # Check if attendance already recorded for today
            self.cursor.execute("SELECT * FROM attendance WHERE id=? AND date=?", 
                              (user_id, date))
            if not self.cursor.fetchone():
                self.cursor.execute("""
                    INSERT INTO attendance (id, name, date, time) 
                    VALUES (?, ?, ?, ?)
                """, (user_id, name, date, time))
                self.conn.commit()
                return True
            return False
        except sqlite3.Error as e:
            print(f"❌ Error recording attendance: {e}")
            return False

    def get_user_name(self, user_id):
        """Get user name by ID."""
        try:
            self.cursor.execute("SELECT name FROM users WHERE id=?", (user_id,))
            result = self.cursor.fetchone()
            return result[0] if result else None
        except sqlite3.Error as e:
            print(f"❌ Error getting user name: {e}")
            return None

    def get_all_users(self):
        """Get all registered users."""
        try:
            self.cursor.execute("SELECT id, name FROM users")
            return {row[0]: row[1] for row in self.cursor.fetchall()}
        except sqlite3.Error as e:
            print(f"❌ Error getting users: {e}")
            return {}

    def get_attendance_records(self, date=None, user_id=None):
        """Get attendance records with optional filters."""
        try:
            query = "SELECT id, name, date, time FROM attendance"
            params = []
            
            # Apply filters
            if date and user_id:
                query += " WHERE date=? AND id=?"
                params = [date, user_id]
            elif date:
                query += " WHERE date=?"
                params = [date]
            elif user_id:
                query += " WHERE id=?"
                params = [user_id]
                
            # Add ordering
            query += " ORDER BY date DESC, time DESC"
            
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
            
        except sqlite3.Error as e:
            print(f"❌ Error getting attendance records: {e}")
            return []

    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None