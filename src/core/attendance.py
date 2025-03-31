"""
Attendance module for Face Recognition Attendance System.
Handles attendance capture logic and processing.
"""

import cv2
import sys
import os
import logging
import time
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
        self.logged_users = {}  # Track users who have been logged with timestamp
        self.logged_strangers = {}  # Track strangers that have been logged with timestamp
        self.log_cooldown = 10  # Cooldown in seconds before logging the same event again
        self.daily_stats = {
            "total_seen": 0, 
            "recognized": 0, 
            "attendance_recorded": 0,
            "strangers_detected": 0
        }
    
    def process_frame(self, frame):
        """Process a video frame for attendance.
        
        Args:
            frame: The camera frame to process
            
        Returns:
            tuple: (processed frame with annotations, number of faces detected)
        """
        # Get face regions from frame
        face_regions = self.face_recognizer.detect_faces(frame)
        current_time = time.time()
        
        # Update stats
        if face_regions:
            self.daily_stats["total_seen"] += 1
        
        # Process each detected face
        for (x, y, w, h, gray_face, color_face) in face_regions:
            # Try to recognize the face with deep learning
            user_id, confidence, is_known = self.face_recognizer.recognize_face(gray_face, color_face)
            
            if user_id and is_known:
                # Update recognized count
                self.daily_stats["recognized"] += 1
                
                # Check if user is active before recording attendance
                user_details = self.db_manager.get_user_details(user_id)
                
                if not user_details:
                    label = f"Unknown ID: {user_id}"
                    is_stranger = True
                elif not user_details.get('active', True):
                    label = f"{user_details['name']} (Inactive)"
                    is_stranger = False
                else:
                    name = user_details['name']
                
                    # Record attendance if not already logged today
                    if user_id not in self.logged_users:
                        success = self.db_manager.record_attendance(user_id, name)
                        if success:
                            self.daily_stats["attendance_recorded"] += 1
                            logging.info(f"✅ Attendance recorded for {name} (ID: {user_id})")
                            self.logged_users[user_id] = current_time
                    else:
                        # Only log "already recorded" if enough time has passed since last log
                        last_log_time = self.logged_users.get(user_id, 0)
                        if current_time - last_log_time > self.log_cooldown:
                            logging.info(f"ℹ️ Attendance already recorded today for {user_id}")
                            self.logged_users[user_id] = current_time  # Update timestamp
                    
                    # Draw box with name and confidence
                    label = f"{name} ({confidence:.1f})"
                    is_stranger = False
            else:
                # This is a stranger - unknown face
                self.daily_stats["strangers_detected"] += 1
                label = f"Unknown ({confidence:.1f})"
                is_stranger = True
                
                # Generate a simple hash based on face position and size to identify unique strangers
                stranger_id = f"stranger_{x}_{y}_{w}_{h}"
                
                # Only log stranger detection if it's a new stranger or enough time has passed
                last_log_time = self.logged_strangers.get(stranger_id, 0)
                if current_time - last_log_time > self.log_cooldown:
                    logging.warning(f"⚠️ Stranger detected with confidence {confidence:.1f}")
                    self.logged_strangers[stranger_id] = current_time  # Update timestamp
            
            # Draw the face box with label
            self.face_recognizer.draw_face_box(frame, x, y, w, h, label, is_stranger)
        
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
            "strangers_detected": self.daily_stats["strangers_detected"],
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
        self.logged_users = {}
        self.logged_strangers = {}
        self.daily_stats = {
            "total_seen": 0, 
            "recognized": 0, 
            "attendance_recorded": 0,
            "strangers_detected": 0
        }
    
    def close(self):
        """Close any open resources."""
        self.db_manager.close()