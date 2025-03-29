"""
Database module for the Attendance Database Management System
"""

from dbms.database.connection import Base, engine, get_db, init_db
from dbms.database.models import Identity, Attendance