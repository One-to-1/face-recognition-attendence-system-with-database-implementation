# System Architecture Document

## Face Recognition Attendance System

### Table of Contents

- [System Architecture Document](#system-architecture-document)
  - [Face Recognition Attendance System](#face-recognition-attendance-system)
    - [Table of Contents](#table-of-contents)
  - [1. Overview](#1-overview)
  - [2. Architectural Goals and Constraints](#2-architectural-goals-and-constraints)
  - [3. System Architecture](#3-system-architecture)
    - [3.1 Component Diagram](#31-component-diagram)
    - [3.2 Architecture Layers](#32-architecture-layers)
    - [3.3 Key Components](#33-key-components)
  - [4. Module Descriptions](#4-module-descriptions)
    - [4.1 Core Module](#41-core-module)
    - [4.2 Database Module](#42-database-module)
    - [4.3 User Interface Module](#43-user-interface-module)
    - [4.4 Utilities Module](#44-utilities-module)
  - [5. Data Flow](#5-data-flow)
    - [5.1 Registration Process](#51-registration-process)
    - [5.2 Attendance Process](#52-attendance-process)
    - [5.3 Reporting Process](#53-reporting-process)
  - [6. Technical Stack](#6-technical-stack)
  - [7. Deployment Architecture](#7-deployment-architecture)

## 1. Overview

This document provides a detailed description of the architectural design of the Face Recognition Attendance System. The system is designed to automate attendance tracking using facial recognition technology in an efficient, user-friendly desktop application.

The architecture follows a modular approach with clear separation of concerns, allowing for maintainability and extensibility. The system is built as a standalone desktop application using Python, with PyQt5 for the user interface, OpenCV for computer vision tasks, and SQLite for database management.

## 2. Architectural Goals and Constraints

The architecture is designed to meet the following goals:

- **Modularity**: Clear separation of components to enable isolated development and testing
- **Maintainability**: Well-organized code structure that facilitates updates and bug fixes
- **Extensibility**: Ability to add new features without major architectural changes
- **Performance**: Efficient processing of image data for real-time face recognition
- **Usability**: Intuitive interfaces that require minimal training

Constraints impacting the architecture include:

- **Offline Operation**: Must function without internet connectivity
- **Local Storage**: All data stored locally in an SQLite database
- **Hardware Limitations**: Must operate efficiently on standard hardware with a webcam
- **Single-User Access**: No concurrent user requirements

## 3. System Architecture

### 3.1 Component Diagram

```txt
┌───────────────────────────────────────────────────────────────────────────┐
│                        Face Recognition Attendance System                 │
└───────────────────────────────────────────────────────────────────────────┘
                                     │
            ┌──────────────────┬─────┴─────┬──────────────────┐
            │                  │           │                  │
┌───────────▼───────────┐ ┌────▼────┐ ┌────▼────┐ ┌──────────▼──────────┐
│      User Interface   │ │  Core   │ │Database │ │      Utilities      │
│      (src/ui)         │ │(src/core)│ │(src/db) │ │     (src/utils)     │
└─────────────────────┬─┘ └────┬────┘ └────┬────┘ └─────────────────────┘
                      │        │           │
     ┌────────────────┼────────┼───────────┼──────────────────┐
     │                │        │           │                  │
┌────▼───┐ ┌──────────▼──┐ ┌───▼───┐ ┌─────▼─────┐ ┌─────────▼────────┐
│  Main  │ │Registration │ │ Face  │ │ Database  │ │ Configuration    │
│ Window │ │  Window     │ │Recog. │ │ Manager   │ │  Settings        │
└────────┘ └─────────────┘ └───────┘ └───────────┘ └──────────────────┘
```

### 3.2 Architecture Layers

The system follows a layered architecture with four main layers:

1. **Presentation Layer (UI)**
   - Responsible for all user interactions
   - Implements the graphical user interface components
   - Communicates with the core layer for business logic

2. **Business Logic Layer (Core)**
   - Contains the application's core functionality
   - Implements face detection and recognition algorithms
   - Manages attendance tracking logic

3. **Data Access Layer (Database)**
   - Manages database connections and operations
   - Implements data access functions
   - Ensures data integrity and consistency

4. **Infrastructure Layer (Utilities/Config)**
   - Provides support functionality
   - Handles configuration and settings
   - Implements common utilities used across layers

### 3.3 Key Components

The system consists of the following key components:

1. **Main Application (app.py)**
   - Entry point of the application
   - Sets up the environment and initializes components
   - Starts the main UI window

2. **UI Components (src/ui/)**
   - Main Window: Central navigation hub
   - Register Window: User registration interface
   - Attendance Window: Live attendance tracking interface
   - Analytics Window: Reporting and data visualization interface
   - Database Window: Database management interface

3. **Core Components (src/core/)**
   - Face Recognition: Face detection and recognition algorithms
   - Model Training: Training functionality for face recognition models
   - Attendance: Attendance recording logic

4. **Database Components (src/database/)**
   - Database Manager: Handles database connections and operations
   - Schema: Defines database structure and constraints

5. **Utility Components (src/utils/)**
   - Image Utils: Image processing utilities
   - Validation: Input validation functions

## 4. Module Descriptions

### 4.1 Core Module

The Core module implements the central business logic of the application.

**Key Files:**

- `face_recognition.py`: Implements face detection and recognition algorithms
- `model_training.py`: Provides functionality to train the face recognition model
- `attendance.py`: Manages attendance recording logic

**Responsibilities:**

- Face detection in images/video streams
- Feature extraction from detected faces
- Face matching against registered users
- Machine learning model management
- Attendance processing logic

**Interactions:**

- Receives camera feed data from the UI layer
- Processes images to detect and recognize faces
- Communicates with the Database layer to retrieve user data and store attendance records
- Returns recognition results to the UI layer

### 4.2 Database Module

The Database module manages data storage and retrieval operations.

**Key Files:**

- `db_manager.py`: Provides database connection and operation functions
- `schema.py`: Defines database tables, indexes, and constraints

**Responsibilities:**

- Managing database connections
- Executing SQL queries
- Ensuring data integrity
- Implementing data access methods
- Managing database schema and migrations

**Interactions:**

- Receives data storage requests from the Core and UI layers
- Returns requested data to other modules
- Maintains the SQLite database file

### 4.3 User Interface Module

The UI module implements all graphical user interfaces of the application.

**Key Files:**

- `main_window.py`: Main application window and navigation hub
- `register_window.py`: Interface for registering new users
- `attendance_window.py`: Interface for taking attendance
- `analytics_window.py`: Interface for viewing reports and analytics
- `database_window.py`: Interface for managing database records
- `style.py`: UI styling and theme definitions
- `icons.py`: Icon resource management

**Responsibilities:**

- Presenting visual interfaces to the user
- Capturing user input
- Displaying recognition and attendance results
- Visualizing reports and analytics
- Managing user navigation through the application

**Interactions:**

- Communicates with Core layer for business logic operations
- Sends requests to Database layer for data operations
- Presents feedback and results to the user

### 4.4 Utilities Module

The Utilities module provides common functionality used throughout the application.

**Key Files:**

- `image_utils.py`: Image processing utility functions
- `validation.py`: Input validation functions

**Responsibilities:**

- Common image processing operations
- Input validation and sanitization
- Utility functions used across multiple modules
- Helper methods for standardized operations

**Interactions:**

- Provides utility functions to all other modules
- Does not typically initiate communication with other modules

## 5. Data Flow

### 5.1 Registration Process

The registration process follows this data flow:

1. User enters registration details in Register Window
2. Register Window captures face images through the webcam
3. Core module's face detection validates the face quality
4. Core module extracts facial features
5. Database module saves user data and face features
6. UI provides feedback on successful registration

```txt
User → UI (Register Window) → Core (Face Recognition) → Core (Feature Extraction) → Database → UI (Feedback)
```

### 5.2 Attendance Process

The attendance process follows this data flow:

1. Attendance Window accesses the webcam feed
2. Core module detects faces in the video stream
3. Core module extracts features from detected faces
4. Core module matches features against database records
5. Core module identifies the user or marks as a stranger
6. Database module records attendance for recognized users
7. UI displays recognition results and attendance confirmation

```txt
Webcam → UI (Attendance Window) → Core (Face Detection) → Core (Recognition) → Database (Check/Record) → UI (Feedback)
```

### 5.3 Reporting Process

The reporting process follows this data flow:

1. User selects report type in Analytics Window
2. Analytics Window sends data request to Database module
3. Database module retrieves requested attendance data
4. Analytics Window processes data and generates visualization
5. UI displays the report to the user

```txt
User → UI (Analytics Window) → Database (Query) → UI (Data Processing) → UI (Visualization)
```

## 6. Technical Stack

The system is built using the following technologies:

- **Programming Language**: Python 3.8+
- **GUI Framework**: PyQt5
- **Computer Vision**: OpenCV
- **Machine Learning**: scikit-learn
- **Database**: SQLite
- **Data Processing**: NumPy
- **Data Visualization**: Matplotlib/PyQtGraph

## 7. Deployment Architecture

The application follows a simple deployment model as a standalone desktop application:

- **Installation**: Single-machine installation with Python interpreter
- **Dependencies**: All required packages specified in requirements.txt
- **Data Storage**: Local folder structure with SQLite database file
- **Configuration**: Local configuration files in the config directory
- **Updates**: Manual updates by replacing application files

No client-server architecture is implemented as the application operates entirely on the local machine.

**Deployment Requirements:**

- Windows 10 or later operating system
- Python 3.8+ with pip package manager
- Webcam with appropriate drivers
- Minimum 4GB RAM, 2GHz processor
- 100MB of free disk space (plus space for user data)
