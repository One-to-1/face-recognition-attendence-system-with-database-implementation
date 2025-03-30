"""
Attendance module for Face Recognition Attendance System.
Handles attendance capture logic and processing.
"""

import cv2
import sys
import os
from datetime import datetime

# Add project root to path to allow imports from config
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.core.face_recognition import FaceRecognizer
from src.database.db_manager import DatabaseManager

class AttendanceProcessor:
    def __init__(self):
        """Initialize components for attendance processing."""
        self.face_recognizer = FaceRecognizer()
        self.db_manager = DatabaseManager()
        self.logged_users = set()  # Keep track of users who have already been logged
    
    def process_frame(self, frame):
        """Process a video frame for attendance."""
        # Get face regions from frame
        face_regions = self.face_recognizer.detect_faces(frame)
        
        # Process each detected face
        for (x, y, w, h, face_img) in face_regions:
            # Try to recognize the face
            user_id, confidence = self.face_recognizer.recognize_face(face_img)
            
            if user_id:
                # Get name from database
                name = self.db_manager.get_user_name(user_id)
                
                if not name:
                    name = f"Unknown ID: {user_id}"
                
                # Record attendance if not already logged
                if user_id not in self.logged_users:
                    success = self.db_manager.record_attendance(user_id, name)
                    if success:
                        print(f"✅ Attendance recorded for {name} (ID: {user_id})")
                        self.logged_users.add(user_id)
                
                # Draw box with name
                label = f"{name} ({confidence:.1f})"
            else:
                # Unknown face
                label = f"Unknown ({confidence:.1f})"
            
            # Draw the face box with label
            self.face_recognizer.draw_face_box(frame, x, y, w, h, label)
        
        return frame, len(face_regions)
    
    def reset_logged_users(self):
        """Reset the set of logged users."""
        self.logged_users = set()
    
    def close(self):
        """Close any open resources."""
        self.db_manager.close()