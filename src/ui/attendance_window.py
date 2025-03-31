"""
Attendance window UI for Face Recognition Attendance System.
"""

import cv2
from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout, QPushButton, 
                           QHBoxLayout, QFrame, QScrollArea, QGridLayout)
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt, QSize

from src.core.attendance import AttendanceProcessor
from src.ui.style import MAIN_STYLE, TITLE_STYLE, CARD_STYLE, MAIN_BUTTON_STYLE
from src.ui.icons import get_camera_icon
from config.settings import CAMERA_INDEX

class AttendanceWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Attendance Capture")
        self.setMinimumSize(800, 600)
        self.setStyleSheet(MAIN_STYLE)
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Title
        title_layout = QHBoxLayout()
        title_label = QLabel("Attendance Capture")
        title_label.setStyleSheet(TITLE_STYLE)
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        
        # Stop button in title area
        self.stop_button = QPushButton()
        self.stop_button.setIcon(get_camera_icon())
        self.stop_button.setIconSize(QPixmap(24, 24).size())
        self.stop_button.setText("Stop Camera")
        self.stop_button.setMinimumHeight(40)
        self.stop_button.setStyleSheet(MAIN_BUTTON_STYLE)
        self.stop_button.clicked.connect(self.stop_camera)
        title_layout.addWidget(self.stop_button)
        
        main_layout.addLayout(title_layout)
        
        # Separator line
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("background-color: #d1d1d1;")
        main_layout.addWidget(line)
        
        # Content area with camera feed and attendance info
        content_layout = QHBoxLayout()
        
        # Camera feed area
        camera_container = QWidget()
        camera_container.setStyleSheet(CARD_STYLE)
        camera_container.setMinimumWidth(500)
        camera_layout = QVBoxLayout(camera_container)
        
        camera_title = QLabel("Camera Feed")
        camera_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        camera_layout.addWidget(camera_title)
        
        self.camera_frame = QLabel()
        self.camera_frame.setAlignment(Qt.AlignCenter)
        self.camera_frame.setMinimumSize(480, 360)
        self.camera_frame.setStyleSheet("background-color: #222; border-radius: 4px;")
        camera_layout.addWidget(self.camera_frame)
        
        self.camera_status = QLabel("Initializing camera...")
        self.camera_status.setAlignment(Qt.AlignCenter)
        camera_layout.addWidget(self.camera_status)
        
        content_layout.addWidget(camera_container, 3)
        
        # Attendance info area
        info_container = QWidget()
        info_container.setStyleSheet(CARD_STYLE)
        info_layout = QVBoxLayout(info_container)
        
        info_title = QLabel("Attendance Records")
        info_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        info_layout.addWidget(info_title)
        
        # Scroll area for attendance logs
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        
        scroll_content = QWidget()
        self.attendance_layout = QVBoxLayout(scroll_content)
        self.attendance_layout.setAlignment(Qt.AlignTop)
        
        scroll_area.setWidget(scroll_content)
        info_layout.addWidget(scroll_area)
        
        self.no_records_label = QLabel("No attendance records yet.")
        self.no_records_label.setAlignment(Qt.AlignCenter)
        self.no_records_label.setStyleSheet("color: #666; padding: 20px 0;")
        self.attendance_layout.addWidget(self.no_records_label)
        
        content_layout.addWidget(info_container, 2)
        
        main_layout.addLayout(content_layout)
        
        # Status bar
        status_bar = QFrame()
        status_bar.setFrameShape(QFrame.StyledPanel)
        status_bar.setStyleSheet("background-color: #f0f0f0; border-radius: 4px; padding: 5px;")
        status_layout = QHBoxLayout(status_bar)
        status_layout.setContentsMargins(10, 5, 10, 5)
        
        self.status_label = QLabel("System ready")
        status_layout.addWidget(self.status_label)
        
        main_layout.addWidget(status_bar)
        
        # Initialize attendance processor
        self.processor = AttendanceProcessor()
        self.attendance_records = set()  # Keep track of logged attendance for display
        
        # Start camera with configured index
        self.cap = cv2.VideoCapture(CAMERA_INDEX)
        if self.cap.isOpened():
            self.camera_status.setText("Camera active. Detecting faces...")
        else:
            self.camera_status.setText("Error: Could not open camera")
            self.status_label.setText("Camera error")
            
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # 30ms refresh rate (approx. 33 fps)

    def update_frame(self):
        """Update the camera feed frame and process for attendance."""
        ret, frame = self.cap.read()
        if not ret:
            self.camera_status.setText("Error: Could not read from camera")
            return

        # Process frame for attendance (detect and recognize faces)
        frame, face_count = self.processor.process_frame(frame)
        
        # Update status based on faces detected
        if face_count > 0:
            self.camera_status.setText(f"Detected {face_count} face(s)")
        else:
            self.camera_status.setText("No faces detected")

        # Convert frame to Qt format for display
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)
        
        # Scale pixmap to fit the label while maintaining aspect ratio
        self.camera_frame.setPixmap(pixmap.scaled(
            self.camera_frame.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        ))
        
        # Update attendance records display
        self.update_attendance_display()

    def update_attendance_display(self):
        """Update the attendance records display."""
        # Get the current attendance records from the processor
        if hasattr(self.processor, 'logged_users') and self.processor.logged_users:
            # If new records are found
            if len(self.processor.logged_users) > len(self.attendance_records):
                # Clear the no records label
                if self.no_records_label.isVisible():
                    self.no_records_label.setVisible(False)
                
                # Add new records
                for user_id in self.processor.logged_users:
                    if user_id not in self.attendance_records:
                        self.attendance_records.add(user_id)
                        
                        # Get user name
                        name = self.processor.db_manager.get_user_name(str(user_id))
                        if not name:
                            name = f"User {user_id}"
                        
                        # Create record item
                        record_frame = QFrame()
                        record_frame.setFrameShape(QFrame.StyledPanel)
                        record_frame.setStyleSheet(
                            "background-color: #e6f7ff; border-radius: 4px; margin-bottom: 5px;"
                        )
                        record_layout = QGridLayout(record_frame)
                        record_layout.setContentsMargins(10, 5, 10, 5)
                        
                        name_label = QLabel(f"<b>{name}</b>")
                        id_label = QLabel(f"ID: {user_id}")
                        id_label.setStyleSheet("color: #666;")
                        
                        record_layout.addWidget(name_label, 0, 0)
                        record_layout.addWidget(id_label, 1, 0)
                        
                        status_label = QLabel("Present ✓")
                        status_label.setStyleSheet("color: green; font-weight: bold;")
                        record_layout.addWidget(status_label, 0, 1, 2, 1, Qt.AlignRight)
                        
                        self.attendance_layout.addWidget(record_frame)
                        
                        # Update status
                        self.status_label.setText(f"Attendance recorded for {name}")

    def stop_camera(self):
        """Stop the camera and release resources."""
        self.timer.stop()
        self.cap.release()
        self.processor.close()
        self.close()
        
    def closeEvent(self, event):
        """Handle window close event."""
        self.stop_camera()
        event.accept()