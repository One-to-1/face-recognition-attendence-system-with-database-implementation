"""
Register window UI for Face Recognition Attendance System.
"""

import cv2
import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, 
                           QPushButton, QMessageBox, QGridLayout,
                           QHBoxLayout, QFrame, QProgressBar, QDialog)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap

from src.database.db_manager import DatabaseManager
from src.core.model_training import ModelTrainer
from config.settings import DATASET_DIR, FACE_SAMPLE_COUNT
from src.ui.style import MAIN_STYLE, TITLE_STYLE, CARD_STYLE, MAIN_BUTTON_STYLE
from src.ui.icons import get_user_plus_icon, get_check_icon
from src.utils.validation import validate_student_name, validate_student_id, sanitize_input

class PoseInstructionDialog(QDialog):
    """Dialog that shows pose instructions and waits for user confirmation."""
    def __init__(self, pose_instruction, pose_index, total_poses, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Pose {pose_index+1}/{total_poses}")
        self.setMinimumSize(400, 250)
        self.setStyleSheet(MAIN_STYLE)
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        
        # Instruction header
        header = QLabel(f"Pose {pose_index+1} of {total_poses}")
        header.setStyleSheet("font-size: 16px; font-weight: bold;")
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # Separator
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)
        
        # Pose instruction
        instruction_frame = QFrame()
        instruction_frame.setStyleSheet("background-color: #e6f2ff; border-radius: 8px;")
        instruction_layout = QVBoxLayout(instruction_frame)
        
        pose_label = QLabel(pose_instruction)
        pose_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #0078d4; padding: 10px;")
        pose_label.setAlignment(Qt.AlignCenter)
        pose_label.setWordWrap(True)
        instruction_layout.addWidget(pose_label)
        
        layout.addWidget(instruction_frame)
        
        # Tips
        tips_label = QLabel("• Position yourself in good lighting\n• Look directly at the camera\n• Keep a neutral expression")
        tips_label.setStyleSheet("color: #606060; margin-top: 10px;")
        layout.addWidget(tips_label)
        
        # Ready button
        self.ready_btn = QPushButton("I'm Ready - Start Capturing")
        self.ready_btn.setMinimumHeight(40)
        self.ready_btn.setStyleSheet(MAIN_BUTTON_STYLE)
        self.ready_btn.clicked.connect(self.accept)
        layout.addWidget(self.ready_btn)

class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Register Student")
        self.setMinimumSize(500, 400)
        self.setStyleSheet(MAIN_STYLE)

        self.db_manager = DatabaseManager()
        self.model_trainer = ModelTrainer()
        
        # Define capture angles for more robust recognition
        self.capture_poses = [
            "Look straight at the camera",
            "Look slightly to the left",
            "Look slightly to the right", 
            "Look slightly up",
            "Look slightly down"
        ]
        # Calculate samples per pose - ensure even distribution
        self.samples_per_pose = FACE_SAMPLE_COUNT // len(self.capture_poses)
        if self.samples_per_pose < 1:
            self.samples_per_pose = 1
            
        # If we have extra samples due to division remainder, distribute them
        self.extra_samples = FACE_SAMPLE_COUNT - (self.samples_per_pose * len(self.capture_poses))
        
        # Make sure total adds up correctly
        self.total_expected_samples = self.samples_per_pose * len(self.capture_poses) + self.extra_samples

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
            "3. For each pose, read the instructions and click 'Ready'\n"
            "4. Stay still while the system captures your face\n"
            "5. Repeat for all required poses"
        )
        instructions_text.setWordWrap(True)
        instructions_text.setStyleSheet("background: transparent;")
        instructions_layout.addWidget(instructions_text)
        
        form_layout.addWidget(instructions_container, 2, 0, 1, 2)
        
        # Progress information
        self.progress_label = QLabel("Capturing face samples:")
        self.progress_label.setVisible(False)
        form_layout.addWidget(self.progress_label, 3, 0, 1, 2)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, FACE_SAMPLE_COUNT)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        form_layout.addWidget(self.progress_bar, 4, 0, 1, 2)
        
        # Pose indicator (now only used for progress display, not instructions)
        self.pose_label = QLabel("")
        self.pose_label.setStyleSheet("color: #0078d4;")
        self.pose_label.setAlignment(Qt.AlignCenter)
        self.pose_label.setVisible(False)
        form_layout.addWidget(self.pose_label, 5, 0, 1, 2)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        self.capture_btn = QPushButton()
        self.capture_btn.setIcon(get_user_plus_icon())
        self.capture_btn.setIconSize(QPixmap(24, 24).size())
        self.capture_btn.setText("Capture Face to Register")
        self.capture_btn.setStyleSheet(MAIN_BUTTON_STYLE)
        self.capture_btn.setMinimumHeight(40)
        buttons_layout.addWidget(self.capture_btn)
        
        form_layout.addLayout(buttons_layout, 6, 0, 1, 2)
        
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
        
        # Check if student ID already exists in database
        if self.db_manager.user_exists(id_):
            QMessageBox.warning(self, "Duplicate ID", 
                              f"Student ID {id_} is already registered. Please use a different ID.")
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

    def wait_for_good_face(self, face_detector, cam, min_faces=1, max_tries=30):
        """Wait until a good face is detected."""
        tries = 0
        while tries < max_tries:
            ret, img = cam.read()
            if not ret:
                return None, None
                
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_detector.detectMultiScale(gray, 1.3, 5)
            
            if len(faces) >= min_faces:
                return img, gray
                
            # Show a cleaner interface with just the camera feed and a simple instruction
            cv2.putText(img, "Position your face in the frame", (20, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            cv2.imshow('Capturing Face...', img)
            cv2.waitKey(100)
            tries += 1
            
        return None, None

    def capture_face(self, name, id_):
        """Capture face samples from multiple angles and register the student."""
        try:
            # Show progress elements
            self.progress_label.setVisible(True)
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(0)
            self.pose_label.setVisible(True)
            self.capture_btn.setEnabled(False)
            
            # Initialize camera
            cam = cv2.VideoCapture(0)
            face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

            # Create dataset directory if it doesn't exist
            if not os.path.exists(DATASET_DIR):
                os.makedirs(DATASET_DIR)

            count = 0
            pose_samples_collected = []  # Keep track of samples per pose
            quit_requested = False
            
            # Capture each pose
            for pose_idx, pose_instruction in enumerate(self.capture_poses):
                # Skip if we've received a quit request
                if quit_requested:
                    break
                    
                # Calculate samples for this pose (distribute any extra samples to the first few poses)
                samples_this_pose = self.samples_per_pose
                if pose_idx < self.extra_samples:
                    samples_this_pose += 1
                
                # Show pose instruction dialog and wait for user to be ready
                pose_dialog = PoseInstructionDialog(
                    pose_instruction, 
                    pose_idx, 
                    len(self.capture_poses), 
                    self
                )
                
                # If user cancels the dialog, stop the capture process
                if pose_dialog.exec_() != QDialog.Accepted:
                    quit_requested = True
                    break
                    
                # Update the current pose indicator
                self.pose_label.setText(f"Capturing pose {pose_idx+1}/{len(self.capture_poses)}")
                
                # Collect samples for this pose
                pose_samples = 0
                # Continue capturing until we get enough samples for this pose
                while pose_samples < samples_this_pose:
                    # Wait for a good face before capturing
                    img, gray = self.wait_for_good_face(face_detector, cam)
                    if img is None:
                        break
                    
                    faces = face_detector.detectMultiScale(gray, 1.3, 5)
                    
                    if len(faces) > 0:
                        # Only process the first detected face
                        (x, y, w, h) = faces[0]
                        
                        count += 1
                        pose_samples += 1
                        
                        # Save the captured face
                        cv2.imwrite(f"{DATASET_DIR}/User.{id_}.{count}_{pose_idx}.jpg", gray[y:y+h, x:x+w])
                        
                        # Create a clean capture display
                        display_img = img.copy()
                        cv2.rectangle(display_img, (x,y), (x+w,y+h), (0, 255, 0), 2)
                        
                        # Display feedback in a cleaner way
                        header_img = cv2.copyMakeBorder(display_img, 50, 0, 0, 0, cv2.BORDER_CONSTANT, value=(240, 240, 240))
                        cv2.putText(header_img, f"Capturing: {pose_samples}/{samples_this_pose}", (20, 30), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 120, 0), 2)
                        
                        cv2.imshow('Capturing Face...', header_img)
                        
                        # Update progress
                        self.update_progress(count)
                    
                    # Exit if 'q' key is pressed
                    if cv2.waitKey(100) & 0xFF == ord('q'):
                        quit_requested = True
                        break
                
                # Store the number of samples we actually collected for this pose
                pose_samples_collected.append((pose_instruction, pose_samples))

            cam.release()
            cv2.destroyAllWindows()

            # Register user in database if we have at least some samples
            if count > 0:
                self.db_manager.register_user(id_, name)
                
                # Train the model with new data
                self.model_trainer.train()
                
                # Reset UI elements
                self.name_input.clear()
                self.id_input.clear()
                self.progress_bar.setValue(count)
                self.pose_label.setVisible(False)
                self.capture_btn.setEnabled(True)
                
                # Prepare detailed message
                pose_details = "\n".join([f"• {pose[0]}: {pose[1]} samples" for pose in pose_samples_collected])
                success_msg = f"{name} (ID: {id_}) registered successfully with {count} face samples:\n\n{pose_details}"
                
                # Show success message
                self.show_status(f"✅ {name} (ID: {id_}) registered successfully with {count} face samples!")
                QMessageBox.information(self, "Success", success_msg)
            else:
                self.show_status("❌ No face samples captured. Please try again.", is_error=True)
                QMessageBox.warning(self, "Warning", "No face samples captured. Please try again.")
                
        except Exception as e:
            print(f"❌ Error during registration: {e}")
            self.capture_btn.setEnabled(True)
            self.pose_label.setVisible(False)
            self.show_status(f"❌ Error: {str(e)}", is_error=True)
            QMessageBox.critical(self, "Error", str(e))