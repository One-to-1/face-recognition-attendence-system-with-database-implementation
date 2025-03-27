from src.database.connection import init_db

def initialize():
    """Initialize the database by creating all tables"""
    init_db()