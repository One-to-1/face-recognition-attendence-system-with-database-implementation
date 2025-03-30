"""
Main window UI for Face Recognition Attendance System.
"""

from PyQt5.QtWidgets import (QMainWindow, QPushButton, QVBoxLayout, QWidget,
                            QLabel, QHBoxLayout, QSpacerItem, QSizePolicy,
                            QFrame)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt

from src.ui.register_window import RegisterWindow
from src.ui.attendance_window import AttendanceWindow
from src.ui.analytics_window import AnalyticsWindow
from src.ui.style import MAIN_STYLE, TITLE_STYLE, CARD_STYLE, MAIN_BUTTON_STYLE
from src.ui.icons import get_user_plus_icon, get_camera_icon, get_chart_icon

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Face Recognition Attendance System")
        self.setMinimumSize(640, 480)
        self.setStyleSheet(MAIN_STYLE)
        
        # Main container
        main_container = QWidget()
        main_layout = QVBoxLayout(main_container)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        title_label = QLabel("Face Recognition Attendance System")
        title_label.setStyleSheet(TITLE_STYLE)
        header_layout.addWidget(title_label)
        main_layout.addLayout(header_layout)
        
        # Horizontal line separator
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("background-color: #d1d1d1;")
        main_layout.addWidget(line)
        
        # Card container
        card_container = QWidget()
        card_container.setStyleSheet(CARD_STYLE)
        card_layout = QVBoxLayout(card_container)
        
        # Description
        desc_label = QLabel("Welcome to the Face Recognition Attendance System. "
                          "Select an option below to get started.")
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(desc_label)
        
        # Button container
        button_layout = QVBoxLayout()
        button_layout.setSpacing(15)
        
        # Register button with icon
        self.register_btn = QPushButton()
        self.register_btn.setIcon(get_user_plus_icon())
        self.register_btn.setIconSize(QPixmap(32, 32).size())
        self.register_btn.setText("Register New Student")
        self.register_btn.setStyleSheet(MAIN_BUTTON_STYLE)
        self.register_btn.setMinimumHeight(50)
        
        # Attendance button with icon
        self.attendance_btn = QPushButton()
        self.attendance_btn.setIcon(get_camera_icon())
        self.attendance_btn.setIconSize(QPixmap(32, 32).size())
        self.attendance_btn.setText("Take Attendance with Camera")
        self.attendance_btn.setStyleSheet(MAIN_BUTTON_STYLE)
        self.attendance_btn.setMinimumHeight(50)
        
        # Analytics button with icon
        self.analytics_btn = QPushButton()
        self.analytics_btn.setIcon(get_chart_icon())
        self.analytics_btn.setIconSize(QPixmap(32, 32).size())
        self.analytics_btn.setText("View Attendance Reports")
        self.analytics_btn.setStyleSheet(MAIN_BUTTON_STYLE)
        self.analytics_btn.setMinimumHeight(50)
        
        # Connect buttons to functions
        self.register_btn.clicked.connect(self.open_register)
        self.attendance_btn.clicked.connect(self.open_attendance)
        self.analytics_btn.clicked.connect(self.open_analytics)
        
        # Add buttons to layout with some space around
        button_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        button_layout.addWidget(self.register_btn)
        button_layout.addWidget(self.attendance_btn)
        button_layout.addWidget(self.analytics_btn)
        button_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Add button layout to card
        card_layout.addLayout(button_layout)
        
        # Add card to main layout
        main_layout.addWidget(card_container)
        
        # Footer
        footer_label = QLabel("Face Recognition Attendance System")
        footer_label.setAlignment(Qt.AlignCenter)
        footer_label.setStyleSheet("color: #666; font-size: 9pt;")
        main_layout.addWidget(footer_label)
        
        # Set central widget
        self.setCentralWidget(main_container)
        
        # Center the window
        self.center_window()

    def open_register(self):
        self.register_window = RegisterWindow()
        self.register_window.show()

    def open_attendance(self):
        self.attendance_window = AttendanceWindow()
        self.attendance_window.show()

    def open_analytics(self):
        self.analytics_window = AnalyticsWindow()
        self.analytics_window.show()
        
    def center_window(self):
        """Center the window on the screen"""
        frame_geometry = self.frameGeometry()
        screen_center = self.screen().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())