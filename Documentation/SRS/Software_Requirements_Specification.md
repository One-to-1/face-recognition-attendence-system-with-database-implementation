# Software Requirements Specification

## Face Recognition Attendance System

### Table of Contents

- [Software Requirements Specification](#software-requirements-specification)
  - [Face Recognition Attendance System](#face-recognition-attendance-system)
    - [Table of Contents](#table-of-contents)
  - [1. Introduction](#1-introduction)
    - [1.1 Purpose](#11-purpose)
    - [1.2 Document Conventions](#12-document-conventions)
    - [1.3 Intended Audience](#13-intended-audience)
    - [1.4 Project Scope](#14-project-scope)
    - [1.5 References](#15-references)
  - [2. Overall Description](#2-overall-description)
    - [2.1 Product Perspective](#21-product-perspective)
    - [2.2 Product Functions](#22-product-functions)
    - [2.3 User Characteristics](#23-user-characteristics)
    - [2.4 Operating Environment](#24-operating-environment)
    - [2.5 Design and Implementation Constraints](#25-design-and-implementation-constraints)
    - [2.6 Assumptions and Dependencies](#26-assumptions-and-dependencies)
  - [3. Specific Requirements](#3-specific-requirements)
    - [3.1 External Interface Requirements](#31-external-interface-requirements)
      - [3.1.1 User Interfaces](#311-user-interfaces)
      - [3.1.2 Hardware Interfaces](#312-hardware-interfaces)
      - [3.1.3 Software Interfaces](#313-software-interfaces)
    - [3.2 Functional Requirements](#32-functional-requirements)
      - [3.2.1 User Registration](#321-user-registration)
      - [3.2.2 Face Recognition and Attendance](#322-face-recognition-and-attendance)
      - [3.2.3 Database Management](#323-database-management)
      - [3.2.4 Analytics and Reporting](#324-analytics-and-reporting)
    - [3.3 Non-Functional Requirements](#33-non-functional-requirements)
      - [3.3.1 Performance Requirements](#331-performance-requirements)
      - [3.3.2 Security Requirements](#332-security-requirements)
      - [3.3.3 Software Quality Attributes](#333-software-quality-attributes)
  - [4. System Features](#4-system-features)
    - [4.1 Face Detection](#41-face-detection)
    - [4.2 Face Recognition](#42-face-recognition)
    - [4.3 Attendance Recording](#43-attendance-recording)
    - [4.4 Reporting and Analytics](#44-reporting-and-analytics)
  - [5. Data Model](#5-data-model)
    - [5.1 Database Schema](#51-database-schema)
    - [5.2 Data Dictionary](#52-data-dictionary)
  - [6. Appendix](#6-appendix)
    - [6.1 File Structure](#61-file-structure)
    - [6.2 Dependencies](#62-dependencies)
    - [6.3 Installation and Setup](#63-installation-and-setup)
    - [6.4 Future Enhancements](#64-future-enhancements)

## 1. Introduction

### 1.1 Purpose

This Software Requirements Specification (SRS) document describes the requirements for the Face Recognition Attendance System. It details the functional and non-functional requirements, constraints, and specifications that will guide the development of the system.

### 1.2 Document Conventions

This document follows standard documentation conventions:

- **Bold text** for emphasis
- `Code style text` for file names, database fields, and technical terms
- *Italic text* for definitions and introducing new terms

### 1.3 Intended Audience

This document is intended for:

- Developers implementing the system
- Project managers overseeing the development
- Testers verifying system functionality
- Users and stakeholders interested in system capabilities

### 1.4 Project Scope

The Face Recognition Attendance System is designed to automate attendance tracking using facial recognition technology. The system will:

- Register users with facial data
- Recognize registered users via webcam
- Record attendance in a database
- Generate attendance reports and analytics
- Provide user-friendly interfaces for all functionality

Out of scope:

- Integration with external HR/student management systems
- Mobile application components
- Cloud-based hosting or synchronization
- Advanced security mechanisms beyond basic authentication

### 1.5 References

- PyQt5 Documentation
- OpenCV Documentation
- SQLite Documentation
- Face Recognition Algorithm References

## 2. Overall Description

### 2.1 Product Perspective

The Face Recognition Attendance System is a standalone desktop application that uses computer vision technology to automate attendance tracking. It replaces manual attendance systems with an automated, efficient solution that reduces human error and saves time.

### 2.2 Product Functions

The main functions of the system include:

1. **User Registration**:
   - Register new users with facial data
   - Associate user profiles with unique identifiers

2. **Face Recognition**:
   - Detect faces in webcam feed
   - Match detected faces with registered user database
   - Identify strangers (unregistered users)

3. **Attendance Management**:
   - Record attendance with date and time stamps
   - Prevent duplicate attendance on the same day
   - Store attendance records in database

4. **Analysis and Reporting**:
   - Generate daily/monthly attendance reports
   - Visualize attendance patterns and statistics
   - Export attendance data for further processing

5. **Database Management**:
   - Add/edit/delete user records
   - View and manage attendance data
   - Backup and restore functionality

### 2.3 User Characteristics

The system is designed for use by the following user types:

1. **Administrators**:
   - Technical understanding of the system
   - Ability to manage users and system settings
   - Responsible for database management

2. **Operators**:
   - Basic computer literacy
   - Responsible for taking attendance via the system
   - Need to understand basic system operation

3. **End Users (Students/Employees)**:
   - Minimal interaction with the system
   - Only need to be present for facial recognition
   - No technical expertise required

### 2.4 Operating Environment

The system will operate in the following environment:

- **Operating System**: Windows 10 or later
- **Hardware**: Computer with webcam, minimum 4GB RAM, 2GHz processor
- **Additional Software**: Python 3.8+, required Python packages
- **Database**: SQLite local database

### 2.5 Design and Implementation Constraints

The system development is constrained by the following factors:

- **Local Operation**: System operates locally without internet dependency
- **Single-User Access**: Only one administrator can access the system at a time
- **Technology Stack**: Python, PyQt5, OpenCV, SQLite
- **Face Recognition Accuracy**: Limited by the quality of facial recognition algorithms and camera input

### 2.6 Assumptions and Dependencies

The system development assumes:

- Users will have necessary hardware (webcam, computer meeting minimum specs)
- Lighting conditions will be adequate for facial recognition
- Users will cooperate with the registration and face recognition process
- External dependencies (PyQt5, OpenCV, etc.) will remain compatible and maintained

## 3. Specific Requirements

### 3.1 External Interface Requirements

#### 3.1.1 User Interfaces

The system will provide the following user interfaces:

1. **Main Window**:
   - Central hub with navigation to all system functions
   - Clear buttons for registration and attendance
   - Access to database management and analytics

2. **Registration Window**:
   - Form for new user information
   - Webcam feed for facial data capture
   - Feedback on registration success/failure

3. **Attendance Window**:
   - Live webcam feed with face detection
   - Real-time recognition and labeling of users
   - Attendance recording confirmation

4. **Database Window**:
   - User management interface
   - Data viewing and editing capabilities
   - Search and filter functionality

5. **Analytics Window**:
   - Graphical reports of attendance data
   - Filtering options for different time periods
   - Export functionality for reports

#### 3.1.2 Hardware Interfaces

The system will interface with the following hardware:

1. **Webcam**:
   - Minimum 720p resolution recommended
   - USB or built-in webcam
   - Automatic detection by the application

2. **Computer System**:
   - Minimum specifications as described in Operating Environment
   - Access to local storage for database and image files

#### 3.1.3 Software Interfaces

The system will interface with:

1. **Operating System**:
   - Access file system for storing data
   - Use system webcam drivers

2. **Database**:
   - SQLite local database
   - File-based storage with SQL queries

3. **External Libraries**:
   - OpenCV for image processing and face detection
   - PyQt5 for GUI components
   - Sklearn for machine learning components of face recognition

### 3.2 Functional Requirements

#### 3.2.1 User Registration

1. **FR-1**: The system shall allow registration of new users with a unique ID and name.
2. **FR-2**: The system shall capture multiple facial images during registration.
3. **FR-3**: The system shall extract and store facial features for recognition.
4. **FR-4**: The system shall validate that the face is clearly visible during registration.
5. **FR-5**: The system shall confirm successful registration to the user.

#### 3.2.2 Face Recognition and Attendance

1. **FR-6**: The system shall detect faces in real-time from webcam feed.
2. **FR-7**: The system shall match detected faces against the database of registered users.
3. **FR-8**: The system shall display the name of recognized users on the interface.
4. **FR-9**: The system shall mark attendance with timestamp when a user is recognized.
5. **FR-10**: The system shall prevent duplicate attendance entries for the same user on the same day.
6. **FR-11**: The system shall identify and mark unregistered faces as "Stranger".

#### 3.2.3 Database Management

1. **FR-12**: The system shall provide an interface to view all registered users.
2. **FR-13**: The system shall allow deactivation and reactivation of users.
3. **FR-14**: The system shall allow viewing of attendance records by date or by user.
4. **FR-15**: The system shall maintain referential integrity between users and attendance records.

#### 3.2.4 Analytics and Reporting

1. **FR-16**: The system shall generate daily attendance reports.
2. **FR-17**: The system shall generate monthly attendance summaries.
3. **FR-18**: The system shall display attendance statistics in graphical format.
4. **FR-19**: The system shall allow filtering of reports by date range.
5. **FR-20**: The system shall provide individual attendance reports for each user.

### 3.3 Non-Functional Requirements

#### 3.3.1 Performance Requirements

1. **NFR-1**: The face detection process shall operate at a minimum of 15 frames per second on standard hardware.
2. **NFR-2**: The face recognition process shall complete within 2 seconds after a face is detected.
3. **NFR-3**: The system shall handle a database of at least 500 users without performance degradation.
4. **NFR-4**: Database queries shall return results within 1 second under normal load.

#### 3.3.2 Security Requirements

1. **NFR-5**: The system shall restrict database management functions to authorized users.
2. **NFR-6**: The system shall store facial recognition data in a format that cannot be easily converted back to images.
3. **NFR-7**: The system shall maintain an audit log of all attendance records.

#### 3.3.3 Software Quality Attributes

1. **NFR-8**: The user interface shall be intuitive and require minimal training.
2. **NFR-9**: The system shall operate without internet connectivity.
3. **NFR-10**: The system shall recover gracefully from crashes without data loss.
4. **NFR-11**: The system shall be easily installable on a standard Windows PC.
5. **NFR-12**: The face recognition accuracy shall exceed 95% under good lighting conditions.

## 4. System Features

### 4.1 Face Detection

The system uses OpenCV's Haar Cascade classifier to detect faces in the webcam feed. This provides real-time face detection capabilities essential for both registration and attendance processes.

**Feature Specifications:**

- Real-time face detection
- Multiple face detection in a single frame
- Face region extraction for further processing
- Visual indication of detected faces with bounding boxes

### 4.2 Face Recognition

The system employs a K-Nearest Neighbors (KNN) algorithm with custom feature extraction for face recognition. This combines histogram-based and LBP-like features to create a robust face recognition system.

**Feature Specifications:**

- Feature extraction from facial regions
- L2 normalization of feature vectors
- KNN-based matching against stored embeddings
- Confidence score calculation for each match
- Stranger detection with threshold-based classification

### 4.3 Attendance Recording

The system records attendance in an SQLite database when a registered user is recognized, ensuring each user is only recorded once per day.

**Feature Specifications:**

- Automatic attendance recording upon recognition
- Date and time stamping of attendance records
- Prevention of duplicate attendance entries
- User feedback on successful attendance recording
- Association of attendance with user profiles

### 4.4 Reporting and Analytics

The system provides comprehensive reporting capabilities to visualize attendance data and extract meaningful insights.

**Feature Specifications:**

- Daily attendance reports
- Monthly attendance summaries
- Individual attendance patterns
- Statistical analysis of attendance data
- Graphical representation of attendance metrics

## 5. Data Model

### 5.1 Database Schema

The system uses an SQLite database with the following main tables:

**Users Table:**

```sql
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    enrollment_date TEXT DEFAULT (datetime('now', 'localtime')),
    last_updated TEXT DEFAULT (datetime('now', 'localtime')),
    active INTEGER DEFAULT 1 NOT NULL CHECK (active IN (0, 1))
)
```

**Attendance Table:**

```sql
CREATE TABLE IF NOT EXISTS attendance (
    attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    id TEXT NOT NULL,
    name TEXT NOT NULL,
    date TEXT NOT NULL,
    time TEXT NOT NULL,
    timestamp INTEGER DEFAULT (strftime('%s','now')),
    FOREIGN KEY (id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE(id, date)
)
```

The database also includes performance optimization through indexes:

- Indexes on attendance date, user ID, and timestamp
- Indexes on user active status and name

### 5.2 Data Dictionary

**Users Table:**

- `id`: Unique identifier for the user
- `name`: Full name of the user
- `enrollment_date`: Date when the user was registered in the system
- `last_updated`: Timestamp of the last update to the user record
- `active`: Boolean flag indicating if the user is active (1) or inactive (0)

**Attendance Table:**

- `attendance_id`: Unique identifier for the attendance record
- `id`: Foreign key referencing the user ID
- `name`: Name of the user (denormalized for reporting ease)
- `date`: Date of attendance
- `time`: Time of attendance
- `timestamp`: Unix timestamp for sorting and calculations

## 6. Appendix

### 6.1 File Structure

The application follows a modular structure:

- `app.py`: Main entry point
- `src/core/`: Core functionality modules
- `src/database/`: Database interaction modules
- `src/ui/`: User interface components
- `src/utils/`: Utility functions
- `config/`: Configuration settings
- `data/`: Storage for datasets and models

### 6.2 Dependencies

The system requires the following Python packages:

- PyQt5 for the GUI
- OpenCV for computer vision tasks
- NumPy for numerical operations
- SQLite3 for database operations
- Scikit-learn for machine learning components

### 6.3 Installation and Setup

Installation requires:

1. Python 3.8 or higher
2. Required packages (see requirements.txt)
3. Webcam with appropriate drivers
4. Sufficient disk space for the database and facial data

### 6.4 Future Enhancements

Potential future enhancements include:

- Multi-factor authentication
- Cloud synchronization options
- Mobile application integration
- Advanced reporting capabilities
- Integration with external systems
