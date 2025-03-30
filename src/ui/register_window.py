"""
Register window UI for Face Recognition Attendance System.
"""

import cv2
import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, 
                           QPushButton, QMessageBox, QGridLayout,
                           QHBoxLayout, QFrame, QProgressBar)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap

from src.database.db_manager import DatabaseManager
from src.core.model_training import ModelTrainer
from config.settings import DATASET_DIR, FACE_SAMPLE_COUNT
from src.ui.style import MAIN_STYLE, TITLE_STYLE, CARD_STYLE, MAIN_BUTTON_STYLE
from src.ui.icons import get_user_plus_icon, get_check_icon
from src.utils.validation import validate_student_name, validate_student_id, sanitize_input

class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Register Student")
        self.setMinimumSize(500, 400)
        self.setStyleSheet(MAIN_STYLE)

        self.db_manager = DatabaseManager()
        self.model_trainer = ModelTrainer()

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title_label = QLabel("Register New Student")
        title_label.setStyleSheet(TITLE_STYLE)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Separator line
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("background-color: #d1d1d1;")
        main_layout.addWidget(line)
        
        # Form container
        form_container = QWidget()
        form_container.setStyleSheet(CARD_STYLE)
        form_layout = QGridLayout(form_container)
        form_layout.setVerticalSpacing(15)
        form_layout.setHorizontalSpacing(10)
        
        # Name input
        name_label = QLabel("Student Name:")
        form_layout.addWidget(name_label, 0, 0)
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter full name")
        self.name_input.setMinimumHeight(35)
        form_layout.addWidget(self.name_input, 0, 1)
        
        # ID input
        id_label = QLabel("Student ID:")
        form_layout.addWidget(id_label, 1, 0)
        
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("Enter numeric ID")
        self.id_input.setMinimumHeight(35)
        form_layout.addWidget(self.id_input, 1, 1)
        
        # Instructions in a single combined block
        instructions_container = QFrame()
        instructions_container.setStyleSheet("background-color: #f0f7ff; border-radius: 4px;")
        instructions_layout = QVBoxLayout(instructions_container)
        instructions_layout.setContentsMargins(10, 10, 10, 10)
        
        instructions_label = QLabel("Instructions:")
        instructions_label.setStyleSheet("font-weight: bold; background: transparent;")
        instructions_layout.addWidget(instructions_label)
        
        instructions_text = QLabel(
            "1. Enter student name and ID\n"
            "2. Click the 'Capture Face & Register' button\n"
            "3. Look at the camera while it captures face samples\n"
            "4. Press 'q' to quit capturing early if needed"
        )
        instructions_text.setWordWrap(True)
        instructions_text.setStyleSheet("background: transparent;")
        instructions_layout.addWidget(instructions_text)
        
        form_layout.addWidget(instructions_container, 2, 0, 1, 2)
        
        # Progress bar (hidden initially)
        self.progress_label = QLabel("Capturing face samples:")
        self.progress_label.setVisible(False)
        form_layout.addWidget(self.progress_label, 3, 0, 1, 2)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, FACE_SAMPLE_COUNT)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        form_layout.addWidget(self.progress_bar, 4, 0, 1, 2)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        self.capture_btn = QPushButton()
        self.capture_btn.setIcon(get_user_plus_icon())
        self.capture_btn.setIconSize(QPixmap(24, 24).size())
        self.capture_btn.setText("Capture Face to Register")
        self.capture_btn.setStyleSheet(MAIN_BUTTON_STYLE)
        self.capture_btn.setMinimumHeight(40)
        buttons_layout.addWidget(self.capture_btn)
        
        form_layout.addLayout(buttons_layout, 5, 0, 1, 2)
        
        # Add form to main layout
        main_layout.addWidget(form_container)
        
        # Connect signals
        self.capture_btn.clicked.connect(self.validate_inputs)
        
        # Status message (hidden initially)
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setVisible(False)
        main_layout.addWidget(self.status_label)
        
    def validate_inputs(self):
        """Validate user inputs before capturing face."""
        name = sanitize_input(self.name_input.text())
        id_ = sanitize_input(self.id_input.text())
        
        name_valid, name_msg = validate_student_name(name)
        id_valid, id_msg = validate_student_id(id_)
        
        if not name_valid:
            QMessageBox.warning(self, "Invalid Name", name_msg)
            return
            
        if not id_valid:
            QMessageBox.warning(self, "Invalid ID", id_msg)
            return
            
        # All inputs are valid, proceed to face capture
        self.capture_face(name, id_)
    
    def update_progress(self, count):
        """Update the progress bar showing face capture progress."""
        self.progress_bar.setValue(count)
        
    def show_status(self, message, is_error=False):
        """Show a status message."""
        self.status_label.setText(message)
        
        if is_error:
            self.status_label.setStyleSheet("color: #d13438; font-weight: bold;")
        else:
            self.status_label.setStyleSheet("color: #107c10; font-weight: bold;")
            
        self.status_label.setVisible(True)
        
        # Hide status after 5 seconds
        QTimer.singleShot(5000, lambda: self.status_label.setVisible(False))

    def capture_face(self, name, id_):
        """Capture face samples and register the student."""
        try:
            # Show progress elements
            self.progress_label.setVisible(True)
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(0)
            self.capture_btn.setEnabled(False)
            
            # Initialize camera
            cam = cv2.VideoCapture(0)
            face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

            # Create dataset directory if it doesn't exist
            if not os.path.exists(DATASET_DIR):
                os.makedirs(DATASET_DIR)

            count = 0
            while True:
                ret, img = cam.read()
                if not ret:
                    break
                    
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_detector.detectMultiScale(gray, 1.3, 5)
                
                for (x, y, w, h) in faces:
                    count += 1
                    
                    # Save the captured face
                    cv2.imwrite(f"{DATASET_DIR}/User.{id_}.{count}.jpg", gray[y:y+h, x:x+w])
                    cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)
                    
                    # Update progress
                    self.update_progress(count)

                cv2.imshow('Registering Face...', img)
                
                # Exit if 'q' key is pressed or enough samples are collected
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break
                elif count >= FACE_SAMPLE_COUNT:
                    break

            cam.release()
            cv2.destroyAllWindows()

            # Register user in database
            self.db_manager.register_user(id_, name)
            
            # Train the model with new data
            self.model_trainer.train()
            
            # Reset UI elements
            self.name_input.clear()
            self.id_input.clear()
            self.progress_bar.setValue(FACE_SAMPLE_COUNT)
            self.capture_btn.setEnabled(True)
            
            # Show success message
            self.show_status(f"✅ {name} (ID: {id_}) registered successfully!")
            QMessageBox.information(self, "Success", f"{name} (ID: {id_}) registered successfully!")
            
        except Exception as e:
            print(f"❌ Error during registration: {e}")
            self.capture_btn.setEnabled(True)
            self.show_status(f"❌ Error: {str(e)}", is_error=True)
            QMessageBox.critical(self, "Error", str(e))