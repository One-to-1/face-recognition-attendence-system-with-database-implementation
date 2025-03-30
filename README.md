# Face Recognition Attendance System

A facial recognition system for automated attendance tracking with database integration.

## Features

- Student registration with facial data capture
- Automated attendance tracking using real-time facial recognition
- Attendance analytics and reporting
- Database storage for student records and attendance data
- Export attendance records to CSV

## Project Structure

```
face-recognition-attendance-system/
│
├── config/                  # Configuration settings
│   └── settings.py          # Application settings
│
├── data/                    # Data storage
│   ├── dataset/             # Face images
│   └── models/              # Trained models
│
├── src/                     # Source code
│   ├── core/                # Core functionality
│   │   ├── attendance.py    # Attendance processing
│   │   ├── face_recognition.py  # Face recognition
│   │   └── model_training.py    # Model training
│   │
│   ├── database/            # Database operations
│   │   └── db_manager.py    # Database management
│   │
│   ├── ui/                  # User interface
│   │   ├── main_window.py       # Main application window
│   │   ├── register_window.py   # Registration UI
│   │   ├── attendance_window.py # Attendance UI
│   │   └── analytics_window.py  # Analytics UI
│   │
│   └── utils/               # Utilities
│       ├── image_utils.py   # Image processing
│       └── validation.py    # Input validation
│
├── tests/                   # Unit tests
├── app.py                   # Application entry point
├── facebase.db              # SQLite database
└── requirements.txt         # Project dependencies
```

## Installation

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the application:
```
python app.py
```

### Register a New Student
1. Click on "Register Student"
2. Enter student name and ID
3. Capture face data

### Record Attendance
1. Click on "Start Attendance"
2. Recognized students will be logged automatically

### View Analytics
1. Click on "View Analytics"
2. Filter by date or student ID
3. Export data to CSV if needed

## Requirements

- Python 3.7+
- OpenCV with contrib modules
- PyQt5
- NumPy
- Pandas
- Matplotlib

## License

This project is licensed under the MIT License - see the LICENSE file for details.