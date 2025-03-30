"""
Database manager for the Face Recognition Attendance System.
Handles all database operations including user registration and attendance recording.
"""

import sqlite3
from datetime import datetime
import os
import sys
import logging

# Add project root to path to allow imports from config
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from config.settings import DB_PATH

# Import schema definitions
from src.database.schema import USERS_TABLE, ATTENDANCE_TABLE, INDEXES, TRIGGERS, QUERY_EXAMPLES

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
            # Enable foreign key support
            self.conn = sqlite3.connect(DB_PATH)
            self.conn.execute("PRAGMA foreign_keys = ON")
            self.cursor = self.conn.cursor()
            logging.info(f"✅ Connected to database: {DB_PATH}")
        except sqlite3.Error as e:
            logging.error(f"❌ Database connection error: {e}")
            raise

    def create_tables(self):
        """Create necessary tables if they don't exist."""
        try:
            # Create tables from schema definitions
            self.cursor.execute(USERS_TABLE)
            self.cursor.execute(ATTENDANCE_TABLE)
            
            # Create indexes for query optimization
            for index in INDEXES:
                self.cursor.execute(index)
                
            # Create triggers
            for trigger in TRIGGERS:
                self.cursor.execute(trigger)
                
            self.conn.commit()
            logging.info("✅ Database tables, indexes, and triggers created successfully")
        except sqlite3.Error as e:
            logging.error(f"❌ Error creating database structure: {e}")
            raise

    def _execute_with_transaction(self, query, params=None):
        """Execute a query with proper transaction handling.
        
        Args:
            query: SQL query string
            params: Query parameters (optional)
            
        Returns:
            cursor: Cursor after query execution
            
        Raises:
            sqlite3.Error: If query execution fails
        """
        if params is None:
            params = []
            
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            return self.cursor
        except sqlite3.Error as e:
            self.conn.rollback()
            logging.error(f"❌ Database error: {e}, Query: {query}, Params: {params}")
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
            logging.error(f"❌ Error checking if user exists: {e}")
            return False

    def register_user(self, user_id, name):
        """Register a new user.
        
        Args:
            user_id: Unique ID for the student
            name: Full name of the student
            
        Returns:
            bool: True if registration was successful, False otherwise
        """
        try:
            self._execute_with_transaction(
                "INSERT INTO users (id, name) VALUES (?, ?)",
                (user_id, name)
            )
            logging.info(f"✅ User registered: {name} (ID: {user_id})")
            return True
        except sqlite3.Error as e:
            logging.error(f"❌ Error registering user: {e}")
            return False

    def update_user(self, user_id, name):
        """Update an existing user's information.
        
        Args:
            user_id: ID of the user to update
            name: New name for the user
            
        Returns:
            bool: True if update was successful, False otherwise
        """
        try:
            self._execute_with_transaction(
                "UPDATE users SET name=? WHERE id=?",
                (name, user_id)
            )
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            logging.error(f"❌ Error updating user: {e}")
            return False

    def deactivate_user(self, user_id):
        """Deactivate a user without deleting their records.
        
        Args:
            user_id: ID of the user to deactivate
            
        Returns:
            bool: True if deactivation was successful, False otherwise
        """
        try:
            self._execute_with_transaction(
                "UPDATE users SET active=0 WHERE id=?",
                (user_id,)
            )
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            logging.error(f"❌ Error deactivating user: {e}")
            return False

    def reactivate_user(self, user_id):
        """Reactivate a previously deactivated user.
        
        Args:
            user_id: ID of the user to reactivate
            
        Returns:
            bool: True if reactivation was successful, False otherwise
        """
        try:
            self._execute_with_transaction(
                "UPDATE users SET active=1 WHERE id=?",
                (user_id,)
            )
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            logging.error(f"❌ Error reactivating user: {e}")
            return False

    def record_attendance(self, user_id, name=None):
        """Record attendance for a user.
        
        Args:
            user_id: ID of the user
            name: Name of the user (optional, will be fetched if not provided)
            
        Returns:
            bool: True if attendance was recorded, False if already recorded today or error
        """
        try:
            # Get current date and time
            now = datetime.now()
            date = now.strftime("%Y-%m-%d")
            time = now.strftime("%H:%M:%S")
            
            # If name not provided, get from database
            if name is None:
                name = self.get_user_name(user_id)
                if name is None:
                    logging.error(f"❌ Cannot record attendance - User ID {user_id} not found")
                    return False
            
            # Check if attendance already recorded for today
            self.cursor.execute(
                "SELECT * FROM attendance WHERE id=? AND date=?", 
                (user_id, date)
            )
            
            if not self.cursor.fetchone():
                # Record new attendance
                self._execute_with_transaction(
                    "INSERT INTO attendance (id, name, date, time) VALUES (?, ?, ?, ?)",
                    (user_id, name, date, time)
                )
                logging.info(f"✅ Attendance recorded: {name} (ID: {user_id})")
                return True
            else:
                logging.info(f"ℹ️ Attendance already recorded today for {user_id}")
                return False
                
        except sqlite3.Error as e:
            logging.error(f"❌ Error recording attendance: {e}")
            return False

    def get_user_name(self, user_id):
        """Get user name by ID.
        
        Args:
            user_id: ID of the user
            
        Returns:
            str: User name or None if not found
        """
        try:
            self.cursor.execute("SELECT name FROM users WHERE id=? AND active=1", (user_id,))
            result = self.cursor.fetchone()
            return result[0] if result else None
        except sqlite3.Error as e:
            logging.error(f"❌ Error getting user name: {e}")
            return None

    def get_user_details(self, user_id):
        """Get complete user details by ID.
        
        Args:
            user_id: ID of the user
            
        Returns:
            dict: User details or None if not found
        """
        try:
            self.cursor.execute(
                "SELECT id, name, enrollment_date, last_updated, active FROM users WHERE id=?", 
                (user_id,)
            )
            result = self.cursor.fetchone()
            
            if result:
                return {
                    'id': result[0],
                    'name': result[1],
                    'enrollment_date': result[2],
                    'last_updated': result[3],
                    'active': bool(result[4])
                }
            return None
            
        except sqlite3.Error as e:
            logging.error(f"❌ Error getting user details: {e}")
            return None

    def get_all_users(self, active_only=True):
        """Get all registered users.
        
        Args:
            active_only: If True, returns only active users
            
        Returns:
            dict: Dictionary mapping user IDs to names
        """
        try:
            if active_only:
                self.cursor.execute("SELECT id, name FROM users WHERE active=1 ORDER BY name")
            else:
                self.cursor.execute("SELECT id, name FROM users ORDER BY name")
                
            return {row[0]: row[1] for row in self.cursor.fetchall()}
            
        except sqlite3.Error as e:
            logging.error(f"❌ Error getting users: {e}")
            return {}

    def get_attendance_records(self, date=None, user_id=None):
        """Get attendance records with optional filters.
        
        Args:
            date: Filter by date (optional)
            user_id: Filter by user ID (optional)
            
        Returns:
            list: List of attendance records
        """
        try:
            query = """
                SELECT a.id, u.name, a.date, a.time 
                FROM attendance a
                JOIN users u ON a.id = u.id
            """
            params = []
            
            # Apply filters
            if date and user_id:
                query += " WHERE a.date=? AND a.id=?"
                params = [date, user_id]
            elif date:
                query += " WHERE a.date=?"
                params = [date]
            elif user_id:
                query += " WHERE a.id=?"
                params = [user_id]
                
            # Add ordering
            query += " ORDER BY a.date DESC, a.time DESC"
            
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
            
        except sqlite3.Error as e:
            logging.error(f"❌ Error getting attendance records: {e}")
            return []

    def get_attendance_statistics(self, period=None):
        """Get attendance statistics.
        
        Args:
            period: 'daily', 'monthly', or 'total' (default)
            
        Returns:
            list: List of statistics records
        """
        try:
            if period == 'daily':
                query = """
                    SELECT date, COUNT(DISTINCT id) as student_count 
                    FROM attendance 
                    GROUP BY date 
                    ORDER BY date DESC
                """
            elif period == 'monthly':
                query = """
                    SELECT strftime('%Y-%m', date) as month, 
                           COUNT(DISTINCT id) as unique_students,
                           COUNT(*) as total_records
                    FROM attendance 
                    GROUP BY month 
                    ORDER BY month DESC
                """
            else:
                query = """
                    SELECT COUNT(DISTINCT date) as total_days,
                           COUNT(DISTINCT id) as total_students,
                           COUNT(*) as total_records
                    FROM attendance
                """
                
            self.cursor.execute(query)
            return self.cursor.fetchall()
            
        except sqlite3.Error as e:
            logging.error(f"❌ Error getting attendance statistics: {e}")
            return []

    def get_user_attendance_summary(self, user_id):
        """Get summary of attendance for a specific user.
        
        Args:
            user_id: ID of the user
            
        Returns:
            dict: Attendance summary for the user
        """
        try:
            # Get total days present
            self.cursor.execute(
                "SELECT COUNT(*) FROM attendance WHERE id=?", 
                (user_id,)
            )
            days_present = self.cursor.fetchone()[0]
            
            # Get first and last attendance dates
            self.cursor.execute(
                "SELECT MIN(date), MAX(date) FROM attendance WHERE id=?", 
                (user_id,)
            )
            first_date, last_date = self.cursor.fetchone()
            
            # Get user details
            user_details = self.get_user_details(user_id)
            
            return {
                'user': user_details,
                'days_present': days_present,
                'first_attendance': first_date,
                'last_attendance': last_date
            }
            
        except sqlite3.Error as e:
            logging.error(f"❌ Error getting user attendance summary: {e}")
            return {}

    def delete_user(self, user_id):
        """Delete a user and all their attendance records.
        
        Args:
            user_id: ID of the user to delete
            
        Returns:
            bool: True if deletion was successful, False otherwise
        """
        try:
            self._execute_with_transaction(
                "DELETE FROM users WHERE id=?", 
                (user_id,)
            )
            return self.cursor.rowcount > 0
            
        except sqlite3.Error as e:
            logging.error(f"❌ Error deleting user: {e}")
            return False

    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None
            logging.info("✅ Database connection closed")