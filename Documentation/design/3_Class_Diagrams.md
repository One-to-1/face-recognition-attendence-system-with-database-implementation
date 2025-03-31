# Class Diagrams

## Overview

This document details the major classes within the Face Recognition Attendance System, their responsibilities, attributes, methods, and relationships. The system follows an object-oriented design pattern with clear separation of concerns between different components.

## Core Classes

### FaceRecognizer

The central class responsible for face detection and recognition.

```txt
┌───────────────────────────────────────────────────────┐
│          FaceRecognizer                               │
├───────────────────────────────────────────────────────┤
│ - face_cascade: CascadeClassifier                     │
│ - knn_model: KNeighborsClassifier                     │
│ - feature_dict: dict                                  │
│ - l2_normalizer: Normalizer                           │
├───────────────────────────────────────────────────────┤
│ + __init__()                                          │
│ + initialize_models()                                 │
│ + create_knn_model()                                  │
│ + detect_faces(frame): face_regions                   │
│ + extract_face_features(face_img)                     │
│ + get_lbp_features(gray_img)                          │
│ + recognize_face(gray_face, color_face)               │
│ + draw_face_box(frame, x, y, w, h, label, is_stranger)│
└───────────────────────────────────────────────────────┘
```

**Responsibilities:**

- Detect faces in video frames
- Extract facial features using custom algorithms
- Match detected faces against stored models
- Determine if a detected face belongs to a registered user or a stranger
- Visualize face detection results in frames

**Relationships:**

- Used by AttendanceProcessor for attendance tracking
- Used by ModelTrainer for creating face embeddings

### DatabaseManager

Manages all database operations and provides an interface for other components to interact with the database.

```txt
┌──────────────────────────────────────────┐
│           DatabaseManager                │
├──────────────────────────────────────────┤
│ - connection: sqlite3.Connection         │
│ - cursor: sqlite3.Cursor                 │
├──────────────────────────────────────────┤
│ + __init__()                             │
│ + create_tables()                        │
│ + register_user(id, name)                │
│ + get_all_users()                        │
│ + get_active_users()                     │
│ + get_user_by_id(id)                     │
│ + deactivate_user(id)                    │
│ + reactivate_user(id)                    │
│ + mark_attendance(id, name, date, time)  │
│ + check_attendance(id, date)             │
│ + get_attendance_by_date(date)           │
│ + get_attendance_by_user(id)             │
│ + get_daily_attendance_count()           │
│ + get_monthly_attendance_summary()       │
│ + get_user_attendance_frequency()        │
│ + close()                                │
└──────────────────────────────────────────┘
```

**Responsibilities:**

- Create and manage database tables, indexes, and triggers
- Provide CRUD operations for users
- Record and retrieve attendance information
- Generate attendance reports and statistics

**Relationships:**

- Used by UI components for data retrieval and storage
- Used by AttendanceProcessor for recording attendance
- Used by RegisterWindow for user registration

### AttendanceProcessor

Processes attendance through face recognition.

```txt
┌──────────────────────────────────────────┐
│           AttendanceProcessor            │
├──────────────────────────────────────────┤
│ - face_recognizer: FaceRecognizer        │
│ - db_manager: DatabaseManager            │
├──────────────────────────────────────────┤
│ + __init__()                             │
│ + process_attendance(frame)              │
│ + mark_attendance(id, name)              │
│ + process_live_feed()                    │
│ + get_attendance_report(date)            │
└──────────────────────────────────────────┘
```

**Responsibilities:**

- Process video frames for face detection
- Recognize identified faces
- Mark attendance for recognized users
- Generate attendance reports

**Relationships:**

- Uses FaceRecognizer for face detection and recognition
- Uses DatabaseManager for attendance storage

### ModelTrainer

Responsible for training the face recognition model.

```txt
┌─────────────────────────────────────────┐
│              ModelTrainer               │
├─────────────────────────────────────────┤
│ - face_recognizer: FaceRecognizer       │
│ - dataset_dir: string                   │
│ - embeddings_path: string               │
├─────────────────────────────────────────┤
│ + __init__()                            │
│ + train_model()                         │
│ + extract_features_from_dataset()       │
│ + save_model()                          │
│ + load_model()                          │
└─────────────────────────────────────────┘
```

**Responsibilities:**

- Process training face images
- Extract features from training images
- Build and train the KNN model
- Save and load model data

**Relationships:**

- Uses FaceRecognizer for feature extraction
- Used during system initialization and user registration

## UI Classes

### MainWindow

The primary application window providing access to all functions.

```txt
┌───────────────────────────────┐
│           MainWindow          │
├───────────────────────────────┤
│ - register_btn: QPushButton   │
│ - attendance_btn: QPushButton │
│ - analytics_btn: QPushButton  │
├───────────────────────────────┤
│ + __init__()                  │
│ + open_register()             │
│ + open_attendance()           │
│ + open_analytics()            │
│ + center_window()             │
└───────────────────────────────┘
```

**Responsibilities:**

- Provide the main application interface
- Navigate to other UI components
- Present system functions to the user

**Relationships:**

- Creates instances of RegisterWindow, AttendanceWindow, and AnalyticsWindow as needed

### RegisterWindow

Handles user registration process.

```txt
┌────────────────────────────────────┐
│          RegisterWindow            │
├────────────────────────────────────┤
│ - id_input: QLineEdit              │
│ - name_input: QLineEdit            │
│ - camera_view: QLabel              │
│ - capture_btn: QPushButton         │
│ - save_btn: QPushButton            │
│ - db_manager: DatabaseManager      │
│ - face_recognizer: FaceRecognizer  │
├────────────────────────────────────┤
│ + __init__()                       │
│ + start_camera()                   │
│ + stop_camera()                    │
│ + capture_face()                   │
│ + save_user()                      │
│ + validate_inputs()                │
└────────────────────────────────────┘
```

**Responsibilities:**

- Capture user information and face samples
- Validate input data
- Register new users in the system
- Trigger model training with new face data

**Relationships:**

- Uses DatabaseManager for user storage
- Uses FaceRecognizer for face detection during registration
- Uses ModelTrainer to update the recognition model

### AttendanceWindow

Manages the attendance capture process.

```txt
┌─────────────────────────────────────────────┐
│               AttendanceWindow              │
├─────────────────────────────────────────────┤
│ - camera_view: QLabel                       │
│ - status_label: QLabel                      │
│ - attendance_processor: AttendanceProcessor │
├─────────────────────────────────────────────┤
│ + __init__()                                │
│ + start_camera()                            │
│ + stop_camera()                             │
│ + process_frame()                           │
│ + display_attendance_status(id, name)       │
└─────────────────────────────────────────────┘
```

**Responsibilities:**

- Present live camera feed to the user
- Process video frames for attendance
- Display attendance status and feedback

**Relationships:**

- Uses AttendanceProcessor for attendance recognition and recording
- Indirectly uses FaceRecognizer through AttendanceProcessor

### AnalyticsWindow

Displays attendance reports and statistics.

```txt
┌─────────────────────────────────────┐
│           AnalyticsWindow           │
├─────────────────────────────────────┤
│ - date_selector: QDateEdit          │
│ - report_table: QTableWidget        │
│ - export_btn: QPushButton           │
│ - db_manager: DatabaseManager       │
├─────────────────────────────────────┤
│ + __init__()                        │
│ + load_report(date)                 │
│ + display_daily_report()            │
│ + display_monthly_report()          │
│ + display_user_report()             │
│ + export_report()                   │
└─────────────────────────────────────┘
```

**Responsibilities:**

- Allow users to select report criteria
- Display attendance reports in tabular format
- Generate and export reports
- Visualize attendance statistics

**Relationships:**

- Uses DatabaseManager for report data retrieval

## Utility Classes

### ImageUtils

Provides utility functions for image processing.

```txt
┌─────────────────────────────────────────┐
│             ImageUtils                  │
├─────────────────────────────────────────┤
│ [Static Methods]                        │
├─────────────────────────────────────────┤
│ + resize_image(image, width, height)    │
│ + convert_cv_to_pixmap(cv_img)          │
│ + equalize_histogram(image)             │
│ + apply_preprocessing(image)            │
└─────────────────────────────────────────┘
```

**Responsibilities:**

- Provide common image processing operations
- Convert between different image formats
- Apply preprocessing for better recognition

### Validation

Provides input validation for the application.

```txt
┌─────────────────────────────────────┐
│              Validation             │
├─────────────────────────────────────┤
│ [Static Methods]                    │
├─────────────────────────────────────┤
│ + validate_id(id): bool             │
│ + validate_name(name): bool         │
│ + validate_date(date): bool         │
│ + sanitize_input(input): string     │
└─────────────────────────────────────┘
```

**Responsibilities:**

- Validate user inputs
- Prevent invalid data entry
- Sanitize inputs for security

## Class Relationship Diagram

```txt
┌───────────┐         ┌───────────────┐         ┌───────────────┐
│MainWindow │─creates→│RegisterWindow │←uses────│ModelTrainer   │
└───────────┘         └───────────────┘         └───────────────┘
     │                       │                          │
     │                       │                          │
     │                       ↓                          │
     │               ┌───────────────┐                  │
     │               │DatabaseManager│←─────────────────┘
     │               └───────────────┘                  
     │                       ↑                          
     │                       │                          
     │                       │                          
     │               ┌────────────────┐         ┌───────────────────┐
     └───creates────→│AttendanceWindow│──uses──→│AttendanceProcessor│
                     └────────────────┘         └───────────────────┘
                            │                          │
                            │                          ↓
                            │                  ┌───────────────┐
                            └─creates─────────→│FaceRecognizer │
                                               └───────────────┘
                                                       ↑
     ┌───────────┐                             ┌───────────────┐
     │MainWindow │─creates────────────────────→│AnalyticsWindow│
     └───────────┘                             └───────────────┘

```

## Design Patterns Used

1. **Singleton Pattern**: Used for DatabaseManager to ensure a single database connection.

2. **Factory Method**: Used in the FaceRecognizer for creating different feature extraction techniques.

3. **Observer Pattern**: Used in the UI for updating the display when attendance is marked.

4. **MVC Pattern**: The system follows a loose Model-View-Controller pattern:
   - Model: DatabaseManager and data classes
   - View: MainWindow, RegisterWindow, etc.
   - Controller: AttendanceProcessor, FaceRecognizer, etc.

## Implementation Considerations

1. **Lazy Loading**: FaceRecognizer loads models only when needed to improve startup time.

2. **Error Handling**: Each class has comprehensive error handling to maintain system stability.

3. **Resource Management**: Camera and database connections are properly managed to prevent resource leaks.

4. **Extensibility**: The system is designed to be extended with new features without modifying existing code.
