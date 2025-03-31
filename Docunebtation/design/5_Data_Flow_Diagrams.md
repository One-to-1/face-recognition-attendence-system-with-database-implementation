# Data Flow Diagrams

## Overview

This document illustrates the flow of data through the Face Recognition Attendance System using Data Flow Diagrams (DFDs). These diagrams help visualize how data moves between different components and processes within the system.

## System Context Diagram (Level 0)

The highest-level view of the system showing its interactions with external entities.

```txt
                 ┌──────────────┐
                 │              │
    Student ────►│              │
    Admin   ────►│ Face         │
                 │ Recognition  │
                 │ Attendance   │
                 │ System       │◄───── Camera
                 │              │
                 │              │
                 └──────────────┘
                        │
                        │
                        ▼
                    Reports
```

## Main Process Flow (Level 1)

Decomposition of the system into its primary processes.

```txt
                                     ┌─────────────┐
                                     │             │
                                     │   Camera    │
                                     │   Input     │
                                     │             │
                                     └──────┬──────┘
                                            │
                                            │ Video Frames
                                            ▼
┌─────────────┐    User Data     ┌─────────────────┐     Face Images     ┌─────────────┐
│             │───────────────►  │                 │ ──────────────────► │             │
│             │                  │                 │                     │             │
│  User       │                  │  Registration   │                     │ Face        │
│  Interface  │ ◄────────────────┤                 │ ◄─────────────────  │ Detection & │
│             │   Feedback       │                 │    Feature Data     │ Recognition │
│             │                  │                 │                     │             │
└─────┬───────┘                  └────────┬────────┘                     └──────┬──────┘
      │                                   │                                     │
      │                                   │ User Records                        │ Recognition
      │                                   ▼                                     │ Results
      │                           ┌─────────────────┐                           │
      │                           │                 │                           │
      │    Query Parameters       │                 │                           │
      └─────────────────────────► │    Database     │ ◄─────────────────────────┘
                                  │    Manager      │       Attendance Records
                                  │                 │
                                  └────────┬────────┘
                                           │
                                           │ Report Data
                                           ▼
                                  ┌─────────────────┐
                                  │                 │
                                  │    Reports &    │
                                  │    Analytics    │
                                  │                 │
                                  └─────────────────┘
```

## Registration Process (Level 2)

Detailed flow of the user registration process.

```txt
┌─────────────┐              ┌───────────────┐              ┌───────────────┐
│             │  Form Data   │               │ User Data    │               │
│ Register UI │─────────────►│ Input         │─────────────►│ Validation    │
│             │              │ Collection    │              │               │
└─────────────┘              └───────────────┘              └───────┬───────┘
                                                                    │
                                  ┌─────────────────────────────────┘
                                  │ Validated Data
                                  ▼
┌─────────────┐              ┌───────────────┐              ┌───────────────┐
│             │  Face Images │               │ Face         │               │
│ Camera      │─────────────►│ Face          │─────────────►│ Feature       │
│ Interface   │              │ Capture       │              │ Extraction    │
└─────────────┘              └───────────────┘              └───────┬───────┘
                                                                    │
                                                                    │ Features
                                                                    ▼
┌─────────────┐              ┌───────────────┐              ┌───────────────┐
│             │  User Record │               │ Model Data   │               │
│ Database    │◄─────────────┤ User Record   │◄─────────────│ Model         │
│ Storage     │              │ Creation      │              │ Training      │
└─────────────┘              └───────────────┘              └───────────────┘
```

## Attendance Capture Process (Level 2)

Detailed flow of the attendance marking process.

```txt
┌─────────────┐              ┌───────────────┐              ┌───────────────┐
│             │  Video Feed  │               │ Video Frames │               │
│ Camera      │─────────────►│ Frame         │─────────────►│ Face          │
│ Interface   │              │ Capture       │              │ Detection     │
└─────────────┘              └───────────────┘              └───────┬───────┘
                                                                   │
                                                                   │ Detected Faces
                                                                   ▼
┌─────────────┐              ┌───────────────┐              ┌───────────────┐
│             │  User IDs    │               │ Face Features│               │
│ User        │◄─────────────┤ Face          │◄─────────────│ Feature       │
│ Recognition │              │ Recognition   │              │ Extraction    │
└──────┬──────┘              └───────────────┘              └───────────────┘
       │
       │ User ID + Confidence
       ▼
┌─────────────┐              ┌───────────────┐              ┌───────────────┐
│             │  Attendance  │               │ Validation   │               │
│ Attendance  │─────────────►│ Attendance    │─────────────►│ Database      │
│ Processing  │  Record      │ Validation    │  Result      │ Storage       │
└─────────────┘              └───────────────┘              └───────────────┘
```

## Analytics Process (Level 2)

Detailed flow of the analytics and reporting process.

```txt
┌─────────────┐              ┌───────────────┐              ┌───────────────┐
│             │  Query       │               │ SQL Queries  │               │
│ Analytics   │─────────────►│ Report        │─────────────►│ Database      │
│ Interface   │  Parameters  │ Generator     │              │ Query         │
└─────────────┘              └───────┬───────┘              └───────┬───────┘
                                     │                              │
                                     └──────────────────────────────┘
                                                   │
                                                   │ Raw Data
                                                   ▼
┌─────────────┐              ┌───────────────┐              ┌───────────────┐
│             │  Visualized  │               │ Processed    │               │
│ Display     │◄─────────────┤ Data          │◄─────────────│ Data          │
│ Interface   │  Data        │ Visualization │  Data        │ Processing    │
└─────────────┘              └───────────────┘              └───────────────┘
                                     ▲
                                     │
                                     │ Export Request
                                     │
                              ┌──────┴──────┐
                              │             │
                              │ Report      │
                              │ Export      │
                              │             │
                              └─────────────┘
```

## Database Interaction Flow

Flow of data between the system and the database.

```txt
┌─────────────┐              ┌───────────────┐              ┌───────────────┐
│             │  SQL         │               │ Database     │               │
│ Application │─────────────►│ Database      │─────────────►│ SQLite        │
│ Logic       │  Queries     │ Manager       │  Commands    │ Database      │
└─────────────┘              └───────┬───────┘              └───────┬───────┘
       ▲                             │                              │
       │                             │                              │
       └─────────────────────────────┘◄─────────────────────────────┘
                 Query Results                 Data Rows
```

## Face Recognition Data Flow

Detailed flow of data through the face recognition process.

```txt
┌─────────────┐              ┌───────────────┐              ┌───────────────┐
│             │  Image       │               │ Detected     │               │
│ Video       │─────────────►│ Face          │─────────────►│ Face          │
│ Frame       │              │ Detection     │  Faces       │ Preprocessing │
└─────────────┘              └───────────────┘              └───────┬───────┘
                                                                   │
                                                                   │ Processed Faces
                                                                   ▼
┌─────────────┐              ┌───────────────┐              ┌───────────────┐
│             │  Identity +  │               │ Similarity   │               │
│ User        │◄─────────────┤ KNN           │◄─────────────│ Feature       │
│ Recognition │  Confidence  │ Classifier    │  Scores      │ Extraction    │
└─────────────┘              └───────────────┘              └───────────────┘
                                     ▲
                                     │
                                     │ Model Data
                                     │
                              ┌──────┴──────┐
                              │             │
                              │ Stored Face │
                              │ Features    │
                              │             │
                              └─────────────┘
```

## Security and Error Handling Flows

Flow of data in security and error handling processes.

```txt
┌─────────────┐              ┌───────────────┐              ┌───────────────┐
│             │  Raw         │               │ Sanitized    │               │
│ User        │─────────────►│ Input         │─────────────►│ Application   │
│ Input       │  Input       │ Validation    │  Data        │ Logic         │
└─────────────┘              └───────┬───────┘              └───────────────┘
                                     │
                                     │ Validation Errors
                                     ▼
                              ┌──────┴──────┐
                              │             │
                              │ Error       │
                              │ Handling    │
                              │             │
                              └─────────────┘
```

## Data Storage Flow

Flow of data in the storage and retrieval processes.

```txt
┌─────────────────┐                      ┌───────────────────┐
│                 │  Face Features       │                   │
│ Feature         │───────────────────►  │ Pickle Storage    │
│ Extraction      │                      │ (face_embeddings) │
└─────────────────┘                      └───────────────────┘

┌─────────────────┐                      ┌───────────────────┐
│                 │  User Records        │                   │
│ Registration    │───────────────────►  │ SQLite Database   │
│ Process         │                      │ (users table)     │
└─────────────────┘                      └───────────────────┘

┌─────────────────┐                      ┌───────────────────┐
│                 │  Attendance Records  │                   │
│ Attendance      │───────────────────►  │ SQLite Database   │
│ Process         │                      │ (attendance table)│
└─────────────────┘                      └───────────────────┘
```

## Mobile Data Flow (Future Enhancement)

Flow of data in potential mobile application interaction.

```txt
┌─────────────┐              ┌───────────────┐              ┌───────────────┐
│             │  API         │               │ Database     │               │
│ Mobile      │─────────────►│ REST API      │─────────────►│ Main          │
│ App         │  Requests    │ Server        │  Queries     │ Application   │
└─────────────┘              └───────────────┘              └───────────────┘
       ▲                                                            │
       │                                                            │
       └────────────────────────────────────────────────────────────┘
                               Response Data
```

## Data State Transitions

Overview of how data changes state as it flows through the system.

1. **User Data**:
   - Initial State: Form Input
   - Validated State: Sanitized User Record
   - Stored State: Database Record

2. **Face Data**:
   - Initial State: Camera Image
   - Processed State: Detected Face
   - Feature State: Extracted Features
   - Recognition State: Matched Identity

3. **Attendance Data**:
   - Initial State: Recognition Event
   - Validated State: Unique Daily Record
   - Stored State: Database Record
   - Report State: Aggregated Statistics

## Key Data Transformations

1. **Image to Features**: Raw camera frames → Face regions → Feature vectors
2. **Features to Identity**: Feature vector → Similarity scores → User ID with confidence
3. **Events to Attendance**: Recognition events → Validated attendance records → Attendance database
4. **Records to Reports**: Database records → Aggregated statistics → Visual reports
