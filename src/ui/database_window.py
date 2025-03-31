"""
Database management window UI for Face Recognition Attendance System.
This window provides functionality for managing students in the database,
including updating information, activating/deactivating students, and deleting records.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QLineEdit, QFrame,
    QHeaderView, QMessageBox, QComboBox, QFormLayout,
    QDialog, QTabWidget, QSplitter, QGroupBox
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QColor

from src.database.db_manager import DatabaseManager
from src.ui.style import MAIN_STYLE, TITLE_STYLE, CARD_STYLE, MAIN_BUTTON_STYLE
from src.ui.icons import get_database_icon, get_check_icon, get_close_icon, get_save_icon
from src.utils.validation import validate_student_name, validate_student_id, sanitize_input

class StudentEditDialog(QDialog):
    """Dialog for editing student information."""
    
    def __init__(self, user_id=None, name=None, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.student_name = name
        self.is_new = user_id is None
        
        self.setWindowTitle("Student Information" if self.is_new else "Edit Student")
        self.setMinimumWidth(400)
        self.setStyleSheet(MAIN_STYLE)
        
        layout = QVBoxLayout(self)
        
        # Form layout for inputs
        form_layout = QFormLayout()
        
        # Student ID field
        self.id_input = QLineEdit(self.user_id if self.user_id else "")
        self.id_input.setPlaceholderText("Enter numeric ID")
        self.id_input.setMinimumHeight(30)
        self.id_input.setEnabled(self.is_new)  # Only enable if new student
        form_layout.addRow("Student ID:", self.id_input)
        
        # Student name field
        self.name_input = QLineEdit(self.student_name if self.student_name else "")
        self.name_input.setPlaceholderText("Enter full name")
        self.name_input.setMinimumHeight(30)
        form_layout.addRow("Student Name:", self.name_input)
        
        layout.addLayout(form_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.save_btn = QPushButton("Save")
        self.save_btn.setIcon(get_save_icon())
        self.save_btn.setMinimumHeight(35)
        self.save_btn.setStyleSheet(MAIN_BUTTON_STYLE)
        self.save_btn.clicked.connect(self.accept)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setIcon(get_close_icon())
        self.cancel_btn.setMinimumHeight(35)
        self.cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(button_layout)
        
    def get_values(self):
        """Get the entered values."""
        return {
            'id': self.id_input.text().strip(),
            'name': self.name_input.text().strip()
        }


class DatabaseWindow(QWidget):
    """Window for database management operations."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Database Management")
        self.setMinimumSize(900, 600)
        self.setStyleSheet(MAIN_STYLE)
        
        self.db_manager = DatabaseManager()
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Title
        title_layout = QHBoxLayout()
        title_label = QLabel("Database Management")
        title_label.setStyleSheet(TITLE_STYLE)
        title_layout.addWidget(title_label)
        
        main_layout.addLayout(title_layout)
        
        # Separator line
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("background-color: #d1d1d1;")
        main_layout.addWidget(line)
        
        # Tab widget for different database functions
        self.tab_widget = QTabWidget()
        
        # Student Management tab
        self.students_tab = QWidget()
        self.create_students_tab()
        self.tab_widget.addTab(self.students_tab, "Student Management")
        
        main_layout.addWidget(self.tab_widget)
        
        # Status bar
        status_bar = QFrame()
        status_bar.setFrameShape(QFrame.StyledPanel)
        status_bar.setStyleSheet("background-color: #f0f0f0; border-radius: 4px; padding: 5px;")
        status_layout = QHBoxLayout(status_bar)
        status_layout.setContentsMargins(10, 5, 10, 5)
        
        self.status_label = QLabel("Ready")
        status_layout.addWidget(self.status_label)
        
        main_layout.addWidget(status_bar)
        
        # Load initial data
        self.load_students()
        
    def create_students_tab(self):
        """Create the student management tab content."""
        tab_layout = QVBoxLayout(self.students_tab)
        
        # Top controls section - search and filter
        control_container = QWidget()
        control_container.setStyleSheet(CARD_STYLE)
        control_layout = QHBoxLayout(control_container)
        
        # Search field
        search_label = QLabel("Search:")
        control_layout.addWidget(search_label)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter name or ID")
        self.search_input.setMinimumHeight(30)
        self.search_input.textChanged.connect(self.filter_students)
        control_layout.addWidget(self.search_input)
        
        # Filter by active/inactive
        filter_label = QLabel("Show:")
        control_layout.addWidget(filter_label)
        
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["All Students", "Active Students", "Inactive Students"])
        self.filter_combo.setMinimumHeight(30)
        self.filter_combo.currentIndexChanged.connect(self.filter_students)
        control_layout.addWidget(self.filter_combo)
        
        # Action buttons
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.setMinimumHeight(35)
        self.refresh_btn.setStyleSheet(MAIN_BUTTON_STYLE)
        self.refresh_btn.clicked.connect(self.load_students)
        control_layout.addWidget(self.refresh_btn)
        
        self.add_student_btn = QPushButton("Add New Student")
        self.add_student_btn.setMinimumHeight(35)
        self.add_student_btn.setStyleSheet(MAIN_BUTTON_STYLE)
        self.add_student_btn.clicked.connect(self.add_student)
        control_layout.addWidget(self.add_student_btn)
        
        tab_layout.addWidget(control_container)
        
        # Students table
        table_container = QWidget()
        table_container.setStyleSheet(CARD_STYLE)
        table_layout = QVBoxLayout(table_container)
        
        table_title = QLabel("Students")
        table_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        table_layout.addWidget(table_title)
        
        self.students_count_label = QLabel("Found 0 students")
        table_layout.addWidget(self.students_count_label)
        
        self.students_table = QTableWidget()
        self.students_table.setColumnCount(6)
        self.students_table.setHorizontalHeaderLabels([
            "ID", "Name", "Enrollment Date", "Last Updated", "Status", "Actions"
        ])
        self.students_table.setAlternatingRowColors(True)
        self.students_table.setStyleSheet("alternate-background-color: #f5f5f5; background-color: white;")
        self.students_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.students_table.setEditTriggers(QTableWidget.NoEditTriggers)  # Make table read-only
        self.students_table.setSelectionBehavior(QTableWidget.SelectRows)
        table_layout.addWidget(self.students_table)
        
        tab_layout.addWidget(table_container)
        
    def load_students(self):
        """Load all students from the database."""
        try:
            self.status_label.setText("Loading students...")
            
            # Get all students, including inactive ones
            self.cursor = self.db_manager.conn.cursor()
            self.cursor.execute(
                "SELECT id, name, enrollment_date, last_updated, active FROM users ORDER BY name"
            )
            students = self.cursor.fetchall()
            
            # Store the full dataset
            self.all_students = students
            
            # Apply current filter
            self.filter_students()
            
            self.status_label.setText(f"Loaded {len(students)} students")
            
        except Exception as e:
            self.status_label.setText(f"Error loading students: {str(e)}")
            print(f"Error loading students: {e}")
    
    def filter_students(self):
        """Filter students based on search text and filter combo."""
        search_text = self.search_input.text().lower().strip()
        filter_option = self.filter_combo.currentText()
        
        filtered_students = []
        
        for student in self.all_students:
            # Apply status filter
            if filter_option == "Active Students" and not student[4]:
                continue
            if filter_option == "Inactive Students" and student[4]:
                continue
                
            # Apply search filter (if any)
            if search_text and search_text not in student[0].lower() and search_text not in student[1].lower():
                continue
                
            filtered_students.append(student)
        
        # Update table with filtered data
        self.update_students_table(filtered_students)
    
    def update_students_table(self, students):
        """Update the students table with the provided data."""
        self.students_table.setRowCount(len(students))
        self.students_count_label.setText(f"Found {len(students)} students")
        
        for row_idx, student in enumerate(students):
            # Data columns
            for col_idx, col_data in enumerate(student):
                if col_idx != 4:  # Skip the 'active' column as we display it differently
                    item = QTableWidgetItem(str(col_data))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.students_table.setItem(row_idx, col_idx, item)
            
            # Status column (active/inactive)
            is_active = bool(student[4])
            status_item = QTableWidgetItem("Active" if is_active else "Inactive")
            status_item.setTextAlignment(Qt.AlignCenter)
            status_item.setForeground(QColor("green" if is_active else "red"))
            self.students_table.setItem(row_idx, 4, status_item)
            
            # Actions column (buttons)
            actions_cell = QWidget()
            actions_layout = QHBoxLayout(actions_cell)
            actions_layout.setContentsMargins(5, 2, 5, 2)
            actions_layout.setSpacing(5)
            
            # Edit button
            edit_btn = QPushButton()
            edit_btn.setIcon(get_save_icon())
            edit_btn.setToolTip("Edit student")
            edit_btn.setFixedSize(28, 28)
            edit_btn.clicked.connect(lambda _, s_id=student[0], s_name=student[1]: self.edit_student(s_id, s_name))
            actions_layout.addWidget(edit_btn)
            
            # Activate/Deactivate button
            toggle_btn = QPushButton()
            if is_active:
                toggle_btn.setIcon(get_close_icon())
                toggle_btn.setToolTip("Deactivate student")
            else:
                toggle_btn.setIcon(get_check_icon())
                toggle_btn.setToolTip("Activate student")
            toggle_btn.setFixedSize(28, 28)
            toggle_btn.clicked.connect(lambda _, s_id=student[0], active=is_active: self.toggle_student_status(s_id, active))
            actions_layout.addWidget(toggle_btn)
            
            # Delete button
            delete_btn = QPushButton("Delete")
            delete_btn.setToolTip("Delete student and all records")
            delete_btn.setFixedSize(50, 28)
            delete_btn.setStyleSheet("background-color: #d13438; color: white; border-radius: 2px; padding: 0px;")
            delete_btn.clicked.connect(lambda _, s_id=student[0], s_name=student[1]: self.delete_student(s_id, s_name))
            actions_layout.addWidget(delete_btn)
            
            # Center the action buttons
            actions_layout.setAlignment(Qt.AlignCenter)
            
            # Put the widget with buttons into the table
            self.students_table.setCellWidget(row_idx, 5, actions_cell)
    
    def add_student(self):
        """Add a new student to the database."""
        dialog = StudentEditDialog(parent=self)
        
        if dialog.exec_():
            values = dialog.get_values()
            
            # Validate inputs
            name_valid, name_msg = validate_student_name(values['name'])
            id_valid, id_msg = validate_student_id(values['id'])
            
            if not name_valid:
                QMessageBox.warning(self, "Invalid Name", name_msg)
                return
                
            if not id_valid:
                QMessageBox.warning(self, "Invalid ID", id_msg)
                return
            
            # Check if ID already exists
            if self.db_manager.user_exists(values['id']):
                QMessageBox.warning(self, "Duplicate ID", 
                                   f"Student ID {values['id']} is already registered.")
                return
                
            # Register new user
            if self.db_manager.register_user(values['id'], values['name']):
                self.status_label.setText(f"Student {values['name']} (ID: {values['id']}) added successfully")
                QMessageBox.information(self, "Success", f"Student {values['name']} added successfully.")
                self.load_students()
            else:
                self.status_label.setText(f"Error adding student")
                QMessageBox.critical(self, "Error", "Failed to add student. Please try again.")
    
    def edit_student(self, student_id, student_name):
        """Edit an existing student's information."""
        dialog = StudentEditDialog(student_id, student_name, parent=self)
        
        if dialog.exec_():
            values = dialog.get_values()
            
            # Validate name
            name_valid, name_msg = validate_student_name(values['name'])
            
            if not name_valid:
                QMessageBox.warning(self, "Invalid Name", name_msg)
                return
                
            # Update user
            if self.db_manager.update_user(student_id, values['name']):
                self.status_label.setText(f"Student {values['name']} (ID: {student_id}) updated successfully")
                self.load_students()
            else:
                self.status_label.setText(f"Error updating student")
                QMessageBox.critical(self, "Error", "Failed to update student. Please try again.")
    
    def toggle_student_status(self, student_id, currently_active):
        """Toggle a student's active status."""
        action = "deactivate" if currently_active else "activate"
        confirmation = QMessageBox.question(
            self,
            f"Confirm {action.capitalize()}",
            f"Are you sure you want to {action} student with ID: {student_id}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if confirmation == QMessageBox.Yes:
            success = False
            if currently_active:
                success = self.db_manager.deactivate_user(student_id)
            else:
                success = self.db_manager.reactivate_user(student_id)
                
            if success:
                self.status_label.setText(f"Student (ID: {student_id}) {action}d successfully")
                self.load_students()
            else:
                self.status_label.setText(f"Error {action}ing student")
                QMessageBox.critical(self, "Error", f"Failed to {action} student. Please try again.")
    
    def delete_student(self, student_id, student_name):
        """Delete a student and all their records."""
        confirmation = QMessageBox.warning(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete {student_name} (ID: {student_id}) and all their records?\n\n"
            "This action cannot be undone!",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if confirmation == QMessageBox.Yes:
            # Double-check with another confirmation for safety
            double_check = QMessageBox.critical(
                self,
                "Final Confirmation",
                f"This will PERMANENTLY delete {student_name} and ALL their attendance records.\n\n"
                "Are you absolutely sure?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if double_check == QMessageBox.Yes:
                if self.db_manager.delete_user(student_id):
                    self.status_label.setText(f"Student {student_name} (ID: {student_id}) and all records deleted")
                    QMessageBox.information(self, "Success", "Student deleted successfully.")
                    self.load_students()
                else:
                    self.status_label.setText(f"Error deleting student")
                    QMessageBox.critical(self, "Error", "Failed to delete student. Please try again.")
                    
    def closeEvent(self, event):
        """Handle window close event."""
        self.db_manager.close()
        event.accept()