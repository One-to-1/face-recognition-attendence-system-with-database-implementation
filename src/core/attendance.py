"""
Attendance module for Face Recognition Attendance System.
Handles attendance capture logic and processing.
"""

import cv2
import sys
import os
import logging
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
        self.daily_stats = {"total_seen": 0, "recognized": 0, "attendance_recorded": 0}
    
    def process_frame(self, frame):
        """Process a video frame for attendance.
        
        Args:
            frame: The camera frame to process
            
        Returns:
            tuple: (processed frame with annotations, number of faces detected)
        """
        # Get face regions from frame
        face_regions = self.face_recognizer.detect_faces(frame)
        
        # Update stats
        if face_regions:
            self.daily_stats["total_seen"] += 1
        
        # Process each detected face
        for (x, y, w, h, face_img) in face_regions:
            # Try to recognize the face
            user_id, confidence = self.face_recognizer.recognize_face(face_img)
            
            if user_id:
                # Update recognized count
                self.daily_stats["recognized"] += 1
                
                # Check if user is active before recording attendance
                user_details = self.db_manager.get_user_details(user_id)
                
                if not user_details:
                    label = f"Unknown ID: {user_id}"
                elif not user_details.get('active', True):
                    label = f"{user_details['name']} (Inactive)"
                else:
                    name = user_details['name']
                
                    # Record attendance if not already logged
                    if user_id not in self.logged_users:
                        success = self.db_manager.record_attendance(user_id, name)
                        if success:
                            self.daily_stats["attendance_recorded"] += 1
                            logging.info(f"✅ Attendance recorded for {name} (ID: {user_id})")
                            self.logged_users.add(user_id)
                    
                    # Draw box with name
                    label = f"{name} ({confidence:.1f})"
            else:
                # Unknown face
                label = f"Unknown ({confidence:.1f})"
            
            # Draw the face box with label
            self.face_recognizer.draw_face_box(frame, x, y, w, h, label)
        
        return frame, len(face_regions)
    
    def get_statistics(self):
        """Get attendance processing statistics.
        
        Returns:
            dict: Statistics about today's attendance processing
        """
        # Get today's date
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Get attendance records for today
        today_records = self.db_manager.get_attendance_records(date=today)
        
        # Get unique users attending today
        unique_users_today = len(set([record[0] for record in today_records]))
        
        # Combine our runtime stats with database stats
        stats = {
            "date": today,
            "faces_processed": self.daily_stats["total_seen"],
            "faces_recognized": self.daily_stats["recognized"],
            "attendance_recorded": self.daily_stats["attendance_recorded"],
            "unique_users": unique_users_today,
            "total_records": len(today_records),
        }
        
        return stats
    
    def get_attendance_history(self, days=7):
        """Get attendance history for the past days.
        
        Args:
            days: Number of days to include in the history
            
        Returns:
            list: Daily attendance records
        """
        return self.db_manager.get_attendance_statistics(period="daily")[:days]
    
    def reset_logged_users(self):
        """Reset the set of logged users."""
        self.logged_users = set()
        self.daily_stats = {"total_seen": 0, "recognized": 0, "attendance_recorded": 0}
    
    def close(self):
        """Close any open resources."""
        self.db_manager.close()