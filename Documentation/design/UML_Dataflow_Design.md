# UML and Dataflow Design Document

## Face Recognition Attendance System

### Table of Contents

- [UML and Dataflow Design Document](#uml-and-dataflow-design-document)
  - [Face Recognition Attendance System](#face-recognition-attendance-system)
    - [Table of Contents](#table-of-contents)
  - [1. Introduction](#1-introduction)
  - [2. Class Diagram (UML)](#2-class-diagram-uml)
    - [2.1 UI Module](#21-ui-module)
    - [2.2 Core Module](#22-core-module)
    - [2.3 Database Module](#23-database-module)
    - [2.4 Utils Module](#24-utils-module)
  - [3. Sequence Diagrams](#3-sequence-diagrams)
    - [3.1 User Registration](#31-user-registration)
    - [3.2 Attendance Capture](#32-attendance-capture)
    - [3.3 Analytics Generation](#33-analytics-generation)
  - [4. Data Flow Diagrams](#4-data-flow-diagrams)
    - [4.1 System Level Data Flow](#41-system-level-data-flow)
    - [4.2 Registration Process Data Flow](#42-registration-process-data-flow)
    - [4.3 Attendance Process Data Flow](#43-attendance-process-data-flow)
  - [5. State Diagrams](#5-state-diagrams)
    - [5.1 Application State](#51-application-state)
    - [5.2 Attendance Session State](#52-attendance-session-state)
  - [6. Data Model](#6-data-model)

## 1. Introduction

This document provides detailed UML (Unified Modeling Language) and data flow diagrams for the Face Recognition Attendance System. It visualizes the relationships between system components, illustrates process flows, and depicts system states to aid in understanding the system architecture and interactions.

## 2. Class Diagram (UML)

The following class diagram represents the main classes in the system and their relationships:

```txt
+------------------+       +------------------+        +-----------------+
|   MainWindow     |------>|  RegisterWindow  |------->| FaceRecognizer  |
+------------------+       +------------------+        +-----------------+
        |                          |                          |
        |                          |                          |
        v                          v                          v
+------------------+       +-----------------+        +-----------------+
| AttendanceWindow |------>| AttendanceProc. |------->| DatabaseManager |
+------------------+       +-----------------+        +-----------------+
        |                                                     ^
        |                                                     |
        v                                                     |
+------------------+       +-----------------+                |
| AnalyticsWindow  |------>| DatabaseWindow  |----------------+
+------------------+       +-----------------+
```

### 2.1 UI Module

```txt
+------------------+
|   MainWindow     |
+------------------+
| - register_btn   |
| - attendance_btn |
| - analytics_btn  |
| - database_btn   |
+------------------+
| + open_register()|
| + open_attendance|
| + open_analytics()|
| + open_database()|
| + center_window()|
+------------------+
        ^
        |
        |
+------------------+     +------------------+     +------------------+     +------------------+
| RegisterWindow   |     | AttendanceWindow |     | AnalyticsWindow  |     | DatabaseWindow   |
+------------------+     +------------------+     +------------------+     +------------------+
| - capture_btn    |     | - start_btn      |     | - period_combo   |     | - student_table  |
| - save_btn       |     | - stop_btn       |     | - export_btn     |     | - add_student_btn|
| - name_input     |     | - video_feed     |     | - charts         |     | - refresh_btn    |
+------------------+     +------------------+     +------------------+     +------------------+
| + start_capture()|     | + start_camera() |     | + load_data()    |     | + load_students()|
| + save_student() |     | + stop_camera()  |     | + generate_chart()|     | + add_student() |
| + process_frame()|     | + process_frame()|     | + export_data()  |     | + edit_student() |
+------------------+     +------------------+     +------------------+     +------------------+
```

### 2.2 Core Module

```txt
+------------------+     +------------------+
| FaceRecognizer   |     | ModelTrainer     |
+------------------+     +------------------+
| - face_detector  |     | - dataset_path   |
| - face_recognizer|     | - model_path     |
| - user_db        |     | - face_detector  |
+------------------+     +------------------+
| + detect_faces() |     | + prepare_data() |
| + recognize_face()|     | + train_model()  |
| + extract_feat() |     | + save_model()   |
| + load_model()   |     | + validate_model()|
+------------------+     +------------------+
        ^                        ^
        |                        |
        +------------+-----------+
                     |
              +------------------+
              | AttendanceProc   |
              +------------------+
              | - face_recognizer|
              | - db_manager     |
              | - logged_users   |
              | - daily_stats    |
              +------------------+
              | + process_frame()|
              | + record_attend()|
              | + get_statistics()|
              +------------------+
```

### 2.3 Database Module

```txt
+------------------+
| DatabaseManager  |
+------------------+
| - conn           |
| - cursor         |
+------------------+
| + connect()      |
| + create_tables()|
| + user_exists()  |
| + register_user()|
| + record_attend()|
| + get_all_users()|
| + get_statistics()|
+------------------+
```

### 2.4 Utils Module

```txt
+------------------+     +------------------+
| ImageUtils       |     | Validation       |
+------------------+     +------------------+
| + resize()       |     | + validate_name()|
| + normalize()    |     | + validate_id()  |
| + add_overlay()  |     | + sanitize_input()|
| + convert_format()|     |                  |
+------------------+     +------------------+
```

## 3. Sequence Diagrams

### 3.1 User Registration

```txt
┌─────┐          ┌───────────────┐          ┌────────────┐          ┌────────────┐          ┌─────────────┐
│User │          │RegisterWindow │          │FaceRecog.  │          │ModelTrainer│          │DatabaseMgr  │
└──┬──┘          └───────┬───────┘          └─────┬──────┘          └─────┬──────┘          └──────┬──────┘
   │  Enter Details     │                         │                       │                        │
   │─────────────────>  │                         │                       │                        │
   │                    │                         │                       │                        │
   │  Start Capture     │                         │                       │                        │
   │─────────────────>  │                         │                       │                        │
   │                    │  capture_frames()       │                       │                        │
   │                    │────────────────────>    │                       │                        │
   │                    │                         │                       │                        │
   │                    │  detect_faces()         │                       │                        │
   │                    │────────────────────>    │                       │                        │
   │                    │  <face detected>        │                       │                        │
   │                    │ <───────────────────    │                       │                        │
   │  Save Student      │                         │                       │                        │
   │─────────────────>  │                         │                       │                        │
   │                    │  extract_features()     │                       │                        │
   │                    │────────────────────>    │                       │                        │
   │                    │  <feature vectors>      │                       │                        │
   │                    │ <───────────────────    │                       │                        │
   │                    │                         │  update_model()       │                        │
   │                    │─────────────────────────────────────────────>   │                        │
   │                    │                         │                       │  <model updated>       │
   │                    │                         │                       │ <────────────────      │
   │                    │                         │                       │                        │
   │                    │  register_user()        │                       │                        │
   │                    │───────────────────────────────────────────────────────────────>          │
   │                    │                         │                       │                        │
   │                    │                         │                       │         <saved>        │
   │  <success message> │                         │                       │         <───────       │
   │ <────────────────  │                         │                       │                        │
┌──┴──┐          ┌───────┴───────┐          ┌─────┴──────┐          ┌─────┴──────┐          ┌──────┴──────┐
│User │          │RegisterWindow │          │FaceRecog.  │          │ModelTrainer│          │DatabaseMgr  │
└─────┘          └───────────────┘          └────────────┘          └────────────┘          └─────────────┘
```

### 3.2 Attendance Capture

```txt
┌─────┐          ┌───────────────┐          ┌────────────┐          ┌─────────────┐
│User │          │AttendanceWin  │          │AttendProc  │          │DatabaseMgr  │
└──┬──┘          └───────┬───────┘          └─────┬──────┘          └──────┬──────┘
   │  Start Attendance   │                        │                        │
   │─────────────────>   │                        │                        │
   │                     │                        │                        │
   │                     │  start_camera()        │                        │
   │                     │────────────────────>   │                        │
   │                     │                        │                        │
   │                     │   <camera started>     │                        │
   │                     │  <────────────────     │                        │
   │                     │                        │                        │
   │                     │  process_frame()       │                        │
   │                     │────────────────────>   │                        │
   │                     │                        │                        │
   │                     │                        │  detect_faces()        │
   │                     │                        │ ───────────────────>   │
   │                     │                        │  <faces detected>      │
   │                     │                        │ <───────────────────   │
   │                     │                        │                        │
   │                     │                        │  recognize_faces()     │
   │                     │                        │ ───────────────────>   │
   │                     │                        │  <users identified>    │
   │                     │                        │ <───────────────────   │
   │                     │                        │                        │
   │                     │                        │  record_attendance()   │
   │                     │                        │ ───────────────────────────>
   │                     │                        │                        │
   │                     │                        │                        │  <recorded>
   │                     │                        │                        │  <───────
   │                     │                        │                        │
   │                     │  <processing results>  │                        │
   │                     │  <──────────────────   │                        │
   │                     │                        │                        │
   │  <display results>  │                        │                        │
   │  <───────────────   │                        │                        │
┌──┴──┐          ┌───────┴───────┐          ┌─────┴──────┐          ┌──────┴──────┐
│User │          │AttendanceWin  │          │AttendProc  │          │DatabaseMgr  │
└─────┘          └───────────────┘          └────────────┘          └─────────────┘
```

### 3.3 Analytics Generation

```txt
┌─────┐          ┌───────────────┐          ┌─────────────┐
│User │          │AnalyticsWin   │          │DatabaseMgr  │
└──┬──┘          └───────┬───────┘          └──────┬──────┘
   │  Request Reports    │                         │
   │─────────────────>   │                         │
   │                     │                         │
   │                     │  get_statistics()       │
   │                     │─────────────────────────────>
   │                     │                         │
   │                     │  <attendance data>      │
   │                     │  <────────────────────────────
   │                     │                         │
   │                     │  process_data()         │
   │                     │ ──────────┐            │
   │                     │           │            │
   │                     │ <─────────┘            │
   │                     │                        │
   │                     │  generate_charts()     │
   │                     │ ──────────┐            │
   │                     │           │            │
   │                     │ <─────────┘            │
   │                     │                         │
   │  <display reports>  │                         │
   │  <───────────────   │                         │
   │                     │                         │
   │  Request Export     │                         │
   │─────────────────>   │                         │
   │                     │  export_to_csv()        │
   │                     │ ──────────┐            │
   │                     │           │            │
   │                     │ <─────────┘            │
   │                     │                         │
   │  <export complete>  │                         │
   │  <───────────────   │                         │
┌──┴──┐          ┌───────┴───────┐          ┌──────┴──────┐
│User │          │AnalyticsWin   │          │DatabaseMgr  │
└─────┘          └───────────────┘          └─────────────┘
```

## 4. Data Flow Diagrams

### 4.1 System Level Data Flow

```txt
                                  ┌──────────────────┐
                                  │                  │
                                  │   User Input     │
                                  │                  │
                                  └────────┬─────────┘
                                           │
                                           │
                                           v
┌──────────────────┐             ┌─────────────────────┐            ┌──────────────────┐
│                  │             │                     │            │                  │
│   Image Data     │─────────────▶  Face Recognition   │────────────▶  Student Data    │
│  (webcam feed)   │             │  Processing System  │            │   (profile)      │
│                  │             │                     │            │                  │
└──────────────────┘             └──────────┬──────────┘            └──────────────────┘
                                           │
                                           │
                                           v
┌──────────────────┐             ┌─────────────────────┐            ┌──────────────────┐
│                  │             │                     │            │                  │
│  Attendance      │◄────────────┤  Database System    │◄───────────┤   Face Model     │
│    Records       │             │                     │            │     Data         │
│                  │             └──────────┬──────────┘            │                  │
└──────────────────┘                       │                       └──────────────────┘
                                           │
                                           v
                                  ┌──────────────────┐
                                  │                  │
                                  │   Reports &      │
                                  │   Analytics      │
                                  │                  │
                                  └──────────────────┘
```

### 4.2 Registration Process Data Flow

```txt
┌──────────────┐     ┌───────────────┐     ┌─────────────────┐     ┌────────────────┐
│              │     │               │     │                 │     │                │
│  Student     │────▶│   Webcam      │────▶│  Face Detection │────▶│ Face Feature   │
│  Details     │     │   Capture     │     │                 │     │ Extraction     │
│              │     │               │     │                 │     │                │
└──────────────┘     └───────────────┘     └─────────────────┘     └────────┬───────┘
                                                                           │
                                                                           │
┌──────────────┐     ┌───────────────┐     ┌─────────────────┐     ┌────────▼───────┐
│              │     │               │     │                 │     │                │
│  Validation  │◀────│   Student     │◀────│  Student Record │◀────│ Model          │
│  Feedback    │     │   Database    │     │  Creation       │     │ Training       │
│              │     │               │     │                 │     │                │
└──────────────┘     └───────────────┘     └─────────────────┘     └────────────────┘
```

### 4.3 Attendance Process Data Flow

```txt
┌──────────────┐     ┌───────────────┐     ┌─────────────────┐     ┌────────────────┐
│              │     │               │     │                 │     │                │
│  Video       │────▶│   Face        │────▶│  Feature        │────▶│ Recognition    │
│  Feed        │     │   Detection   │     │  Extraction     │     │ Matching       │
│              │     │               │     │                 │     │                │
└──────────────┘     └───────────────┘     └─────────────────┘     └────────┬───────┘
                                                                           │
                                                                           │
┌──────────────┐     ┌───────────────┐     ┌─────────────────┐     ┌────────▼───────┐
│              │     │               │     │                 │     │                │
│  Attendance  │◀────│   User        │◀────│  Attendance     │◀────│ User           │
│  Display     │     │   Feedback    │     │  Recording      │     │ Identification │
│              │     │               │     │                 │     │                │
└──────────────┘     └───────────────┘     └─────────────────┘     └────────────────┘
```

## 5. State Diagrams

### 5.1 Application State

```txt
                      ┌───────────────────────┐
                      │                       │
                      │  Application Launch   │
                      │                       │
                      └───────────┬───────────┘
                                  │
                                  │
                                  v
┌───────────────┐      ┌───────────────────────┐      ┌───────────────┐
│               │      │                       │      │               │
│  Registration │◀─────┤      Main Menu        │─────▶│  Attendance   │
│  State        │      │                       │      │  State        │
│               │      └───────────┬───────────┘      │               │
└───────┬───────┘                  │                  └───────┬───────┘
        │                          │                          │
        │                          │                          │
        v                          v                          v
┌───────────────┐      ┌───────────────────────┐      ┌───────────────┐
│               │      │                       │      │               │
│  Database     │◀─────┤      Exit/Shutdown    │      │  Analytics    │
│  Management   │      │                       │      │  State        │
│               │      └───────────────────────┘      │               │
└───────────────┘                                     └───────────────┘
```

### 5.2 Attendance Session State

```txt
┌───────────────┐      ┌───────────────────────┐      ┌───────────────┐
│               │      │                       │      │               │
│  Camera       │─────▶│    Processing         │─────▶│ Recognition   │
│  Initialization│      │    Video Feed        │      │ Processing    │
│               │      │                       │      │               │
└───────────────┘      └───────────────────────┘      └───────┬───────┘
                                                             │
                                                             │
┌───────────────┐      ┌───────────────────────┐      ┌───────▼───────┐
│               │      │                       │      │               │
│  Session      │◀─────┤   User Verification   │◀─────┤  Attendance   │
│  Termination  │      │                       │      │  Recording    │
│               │      └───────────────────────┘      │               │
└───────────────┘                                     └───────────────┘
```

## 6. Data Model

The data model directly corresponds to the database schema defined in the Database Design Document. The main entities and their relationships are:

1. **User Entity**
   - Contains student information
   - Primary key: id (TEXT)
   - Properties: name, enrollment_date, last_updated, active

2. **Attendance Entity**
   - Records attendance instances
   - Primary key: attendance_id (INTEGER)
   - Foreign key: id (references User.id)
   - Properties: name, date, time, timestamp

3. **Face Recognition Data**
   - Not stored directly in the database
   - Stored as serialized models in the filesystem
   - Referenced by User IDs for mapping

Relationship: One-to-Many between Users and Attendance records (a user can have multiple attendance records).
