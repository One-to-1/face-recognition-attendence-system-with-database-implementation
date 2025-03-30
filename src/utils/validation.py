"""
Validation utility functions for Face Recognition Attendance System.
"""

import re

def validate_student_id(student_id):
    """
    Validate student ID format.
    Returns (is_valid, message)
    """
    if not student_id:
        return False, "Student ID cannot be empty"
        
    if not student_id.isdigit():
        return False, "Student ID must contain only digits"
        
    # Add any specific validation rules for your institution
    if len(student_id) < 1 or len(student_id) > 10:
        return False, "Student ID must be between 1 and 10 digits"
        
    return True, "Valid student ID"
    
def validate_student_name(name):
    """
    Validate student name format.
    Returns (is_valid, message)
    """
    if not name:
        return False, "Name cannot be empty"
        
    if len(name) < 2:
        return False, "Name is too short"
        
    if len(name) > 50:
        return False, "Name is too long (max 50 characters)"
        
    # Basic name validation - allows letters, spaces, hyphens, apostrophes
    if not re.match(r'^[A-Za-z\s\-\']+$', name):
        return False, "Name contains invalid characters"
        
    return True, "Valid name"
    
def sanitize_input(input_text):
    """
    Sanitize input to prevent SQL injection and other attacks.
    """
    if not input_text:
        return ""
        
    # Remove potentially dangerous characters
    sanitized = re.sub(r'[;\'\"\\]', '', input_text)
    return sanitized.strip()
    
def validate_date_format(date_str):
    """
    Validate that a date string is in YYYY-MM-DD format.
    Returns (is_valid, message)
    """
    if not date_str:
        return False, "Date cannot be empty"
        
    # Check format using regex
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
        return False, "Date must be in YYYY-MM-DD format"
        
    # Additional validation could check if it's a valid calendar date
    # For simplicity, we're just checking the format
    
    return True, "Valid date format"