# User Interface Design Document

## Face Recognition Attendance System

### Table of Contents

- [User Interface Design Document](#user-interface-design-document)
  - [Face Recognition Attendance System](#face-recognition-attendance-system)
    - [Table of Contents](#table-of-contents)
  - [1. Introduction](#1-introduction)
  - [2. UI Design Principles](#2-ui-design-principles)
  - [3. UI Architecture](#3-ui-architecture)
  - [4. Screen Designs](#4-screen-designs)
    - [4.1 Main Window](#41-main-window)
    - [4.2 Registration Window](#42-registration-window)
    - [4.3 Attendance Window](#43-attendance-window)
    - [4.4 Analytics Window](#44-analytics-window)
    - [4.5 Database Window](#45-database-window)
  - [5. UI Components](#5-ui-components)
    - [5.1 Common Components](#51-common-components)
    - [5.2 Custom Controls](#52-custom-controls)
  - [6. User Flow Diagrams](#6-user-flow-diagrams)
    - [Registration Flow](#registration-flow)
    - [Attendance Flow](#attendance-flow)
    - [Analytics Flow](#analytics-flow)
  - [7. UI Styling](#7-ui-styling)
  - [8. Accessibility Considerations](#8-accessibility-considerations)
  - [9. UI-Business Logic Integration](#9-ui-business-logic-integration)

## 1. Introduction

This document defines the user interface design for the Face Recognition Attendance System. It details the visual components, screen layouts, user flows, and design principles that guide the application's interface implementation. The UI is implemented using PyQt5, a robust framework for creating desktop applications with Python.

## 2. UI Design Principles

The user interface follows these core design principles:

1. **Simplicity**: Clean layouts with focused functionality and minimal distractions
2. **Intuitiveness**: Self-explanatory navigation and controls that require minimal training
3. **Feedback**: Clear visual feedback for user actions and system processes
4. **Consistency**: Uniform visual language and interaction patterns across the application
5. **Efficiency**: Streamlined workflows that minimize the number of clicks for common tasks

## 3. UI Architecture

The UI architecture follows the Model-View separation pattern where:

- **Views** (UI classes) handle user interaction and display
- **Models** (core and database classes) manage data and business logic
- Communication between layers follows a clear request-response pattern

The UI is organized as follows:

```txt
src/ui/
├── __init__.py           # Module initialization
├── main_window.py        # Main application window
├── register_window.py    # User registration interface
├── attendance_window.py  # Attendance taking interface
├── analytics_window.py   # Reporting and analytics interface
├── database_window.py    # Database management interface
├── style.py              # UI styling definitions
└── icons.py              # Icon resource management
```

## 4. Screen Designs

### 4.1 Main Window

The Main Window serves as the central hub for navigating to all system functions.

**Layout Structure:**

```txt
┌─────────────────────────────────────────────────────┐
│ Face Recognition Attendance System        [A] [D]   │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌─────────────────────────────────────────────┐    │
│  │                                             │    │
│  │  Welcome to the Face Recognition            │    │
│  │  Attendance System. Select an option below  │    │
│  │  to get started.                            │    │
│  │                                             │    │
│  │  ┌─────────────────────────────────────┐    │    │
│  │  │    [ICON] Register New Student      │    │    │
│  │  └─────────────────────────────────────┘    │    │
│  │                                             │    │
│  │  ┌─────────────────────────────────────┐    │    │
│  │  │    [ICON] Take Attendance with      │    │    │
│  │  │           Camera                    │    │    │
│  │  └─────────────────────────────────────┘    │    │
│  │                                             │    │
│  └─────────────────────────────────────────────┘    │
│                                                     │
│  Face Recognition Attendance System                 │
└─────────────────────────────────────────────────────┘
```

**Key Elements:**

- Title bar with application name
- Analytics [A] and Database [D] icons in the top right corner
- Card container with application description
- Two main action buttons with icons:
  - Register New Student
  - Take Attendance with Camera
- Footer with application name

**Interactions:**

- Clicking Register button opens the Registration Window
- Clicking Attendance button opens the Attendance Window
- Clicking Analytics icon opens the Analytics Window
- Clicking Database icon opens the Database Window

### 4.2 Registration Window

The Registration Window handles capturing new user data and facial images.

**Layout Structure:**

```txt
┌──────────────────────────────────────────────────┐
│ Register New Student                        [X]  │
├──────────────────────────────────────────────────┤
│ ┌───────────────────┐  ┌───────────────────────┐ │
│ │                   │  │ User ID:              │ │
│ │                   │  │ ┌─────────────────┐   │ │
│ │                   │  │ │User.1           │   │ │
│ │                   │  │ └─────────────────┘   │ │
│ │                   │  │                       │ │
│ │   Webcam Feed     │  │ Full Name:            │ │
│ │                   │  │ ┌─────────────────┐   │ │
│ │                   │  │ │                 │   │ │
│ │                   │  │ └─────────────────┘   │ │
│ │                   │  │                       │ │
│ │                   │  │ ┌─────────────────┐   │ │
│ │                   │  │ │ Capture Images  │   │ │
│ └───────────────────┘  │ └─────────────────┘   │ │
│                        │                       │ │
│ Face Count: 0/10       │ Status: Ready         │ │
│                        │                       │ │
│                        │ ┌─────────────────┐   │ │
│                        │ │     Register    │   │ │
│                        │ └─────────────────┘   │ │
│                        └───────────────────────┘ │
└──────────────────────────────────────────────────┘
```

**Key Elements:**

- Title bar with window name and close button
- Left panel containing:
  - Live webcam feed
  - Face capture count indicator
- Right panel containing:
  - User ID field (auto-generated)
  - Full Name input field
  - Capture Images button
  - Status indicator
  - Register button

**Interactions:**

- Webcam feed shows real-time video with face detection
- Capture Images button takes multiple face images for training
- Register button saves user data and facial features
- Close button returns to Main Window

### 4.3 Attendance Window

The Attendance Window handles face recognition and attendance recording.

**Layout Structure:**

```txt
┌───────────────────────────────────────────────────┐
│ Attendance                                   [X]  │
├───────────────────────────────────────────────────┤
│ ┌───────────────────────────────────────────────┐ │
│ │                                               │ │
│ │                                               │ │
│ │                                               │ │
│ │                                               │ │
│ │               Webcam Feed                     │ │
│ │            with Face Detection                │ │
│ │                                               │ │
│ │                                               │ │
│ │                                               │ │
│ │                                               │ │
│ └───────────────────────────────────────────────┘ │
│                                                   │
│ ┌───────────────────────┐ ┌────────────────────┐  │
│ │ Date: 2025-04-02      │ │  Attendance Mode   │  │
│ └───────────────────────┘ └────────────────────┘  │
│                                                   │
│ Status: Looking for faces...                      │
│                                                   │
│ Recently Recognized:                              │
│ John Doe (User.1) - 10:30:45                      │
└───────────────────────────────────────────────────┘
```

**Key Elements:**

- Title bar with window name and close button
- Large webcam feed with face detection overlay
- Date display showing current date
- Attendance Mode toggle (switch between modes if needed)
- Status message showing current system state
- Recently recognized list showing latest attendance entries

**Interactions:**

- Webcam constantly processes faces and performs recognition
- Recognized faces are highlighted with name and ID
- Attendance is automatically recorded when a face is recognized
- Status message updates based on system activity
- Recent recognitions are listed for verification

### 4.4 Analytics Window

The Analytics Window provides visualization and reporting of attendance data.

**Layout Structure:**

```txt
┌─────────────────────────────────────────────────────┐
│ Attendance Analytics                         [X]    │
├─────────────────────────────────────────────────────┤
│ ┌───────────────┐                                   │
│ │ Report Type:  │ ┌───────────────────────────────┐ │
│ │ ┌───────────┐ │ │                               │ │
│ │ │Daily     ▼│ │ │                               │ │
│ │ └───────────┘ │ │                               │ │
│ │               │ │                               │ │
│ │ Date Range:   │ │         Chart Area            │ │
│ │ From:         │ │                               │ │
│ │ ┌───────────┐ │ │                               │ │
│ │ │2025-04-01 │ │ │                               │ │
│ │ └───────────┘ │ │                               │ │
│ │ To:           │ │                               │ │
│ │ ┌───────────┐ │ │                               │ │
│ │ │2025-04-02 │ │ │                               │ │
│ │ └───────────┘ │ └───────────────────────────────┘ │
│ │               │                                   │
│ │ ┌───────────┐ │ ┌───────────────────────────────┐ │
│ │ │ Generate  │ │ │                               │ │
│ │ └───────────┘ │ │        Data Table             │ │
│ │               │ │                               │ │
│ │ ┌───────────┐ │ │                               │ │
│ │ │  Export   │ │ │                               │ │
│ │ └───────────┘ │ │                               │ │
│ └───────────────┘ └───────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

**Key Elements:**

- Title bar with window name and close button
- Left sidebar containing:
  - Report type dropdown (Daily, Monthly, User-specific)
  - Date range selection
  - Generate button to create reports
  - Export button for exporting data
- Right panel containing:
  - Chart area for graphical representation
  - Data table for detailed records

**Interactions:**

- Report type selection changes available parameters and report format
- Date range selection filters the data period
- Generate button refreshes the report with current parameters
- Export button allows saving reports in various formats

### 4.5 Database Window

The Database Window provides an interface for managing database records.

**Layout Structure:**

```txt
┌─────────────────────────────────────────────────────┐
│ Database Management                          [X]    │
├─────────────────────────────────────────────────────┤
│ ┌───────────────┐ ┌───────────────────────────────┐ │
│ │ View:         │ │                               │ │
│ │ ┌───────────┐ │ │                               │ │
│ │ │Users     ▼│ │ │                               │ │
│ │ └───────────┘ │ │                               │ │
│ │               │ │                               │ │
│ │ Search:       │ │       Database Records        │ │
│ │ ┌───────────┐ │ │          Data Grid            │ │
│ │ │           │ │ │                               │ │
│ │ └───────────┘ │ │                               │ │
│ │               │ │                               │ │
│ │ Filter:       │ │                               │ │
│ │ ┌───────────┐ │ │                               │ │
│ │ │  Active  ▼│ │ │                               │ │
│ │ └───────────┘ │ │                               │ │
│ │               │ └───────────────────────────────┘ │
│ │ Actions:      │ ┌───────────────────────────────┐ │
│ │ ┌───────────┐ │ │                               │ │
│ │ │ Activate  │ │ │                               │ │
│ │ └───────────┘ │ │        Record Details         │ │
│ │ ┌───────────┐ │ │                               │ │
│ │ │Deactivate │ │ │                               │ │
│ │ └───────────┘ │ │                               │ │
│ └───────────────┘ └───────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

**Key Elements:**

- Title bar with window name and close button
- Left sidebar containing:
  - View selector (Users/Attendance)
  - Search field for filtering records
  - Additional filters (Active/All, Date range)
  - Action buttons (Activate, Deactivate)
- Main area containing:
  - Data grid showing database records
  - Record details panel showing selected record information

**Interactions:**

- View selection changes the displayed table
- Search field filters records based on text input
- Filters refine the displayed records based on criteria
- Action buttons apply operations to selected records
- Selecting a record displays its details in the details panel

## 5. UI Components

### 5.1 Common Components

The application uses the following common UI components:

1. **Title Bars**
   - Consistent styling across all windows
   - Window title on the left
   - Close/minimize buttons on the right

2. **Buttons**
   - Primary action buttons: Bold text, accent color background
   - Secondary action buttons: Regular text, lighter background
   - Icon buttons: Icon with tooltip for space-saving actions

3. **Input Fields**
   - Text fields with descriptive labels
   - Validation indicators for invalid input
   - Placeholder text for guidance

4. **Lists and Tables**
   - Alternating row colors for readability
   - Column headers with sort functionality
   - Selection highlighting

5. **Dialog Boxes**
   - Modal dialogs for confirmations
   - Non-blocking notifications for status updates
   - Error dialogs for issue reporting

### 5.2 Custom Controls

The application implements the following custom controls:

1. **Face Detection Canvas**
   - Displays webcam feed with overlay
   - Highlights detected faces with bounding boxes
   - Shows recognition information next to faces
   - Implements real-time update mechanism

2. **Attendance Status Indicator**
   - Visual indicator of attendance recording
   - Green confirmation animation on successful recognition
   - Yellow processing indicator during recognition
   - Red warning for failed recognition attempts

3. **Chart Visualizations**
   - Daily attendance bar charts
   - Monthly attendance trend lines
   - User attendance frequency histograms
   - Interactive chart controls (zoom, tooltip)

## 6. User Flow Diagrams

### Registration Flow

```txt
┌───────────┐     ┌───────────────┐     ┌──────────────┐
│  Main     │     │ Registration  │     │  Capture     │
│  Window   │────►│ Window        │────►│  Images      │
└───────────┘     └───────────────┘     └──────┬───────┘
                                               │
                                               │
                          ┌──────────────┐     │
                          │  Main        │◄────┘
                          │  Window      │
                          └──────────────┘
```

### Attendance Flow

```txt
┌───────────┐     ┌───────────────┐     ┌──────────────┐
│  Main     │     │  Attendance   │     │  Face        │
│  Window   │────►│  Window       │────►│  Recognition │
└───────────┘     └───────────────┘     └──────┬───────┘
                                               │
                  ┌───────────────┐            │
                  │  Record       │◄───────────┘
                  │  Attendance   │
                  └───────────────┘
```

### Analytics Flow

```txt
┌───────────┐     ┌───────────────┐     ┌──────────────┐
│  Main     │     │  Analytics    │     │  Generate    │
│  Window   │────►│  Window       │────►│  Report      │
└───────────┘     └───────────────┘     └──────┬───────┘
                                               │
                                        ┌──────▼───────┐
                                        │  Display     │
                                        │  Results     │
                                        └──────┬───────┘
                                               │
                                        ┌──────▼───────┐
                                        │  Export      │
                                        │  (Optional)  │
                                        └──────────────┘
```

## 7. UI Styling

The application implements a consistent visual style defined in `style.py`:

**Color Palette:**

- Primary Color: #3498db (Blue) - Used for primary actions and highlights
- Secondary Color: #2ecc71 (Green) - Used for success indicators
- Warning Color: #f39c12 (Orange) - Used for warnings
- Error Color: #e74c3c (Red) - Used for errors
- Background Color: #f5f5f5 (Light Gray) - Main background
- Text Color: #333333 (Dark Gray) - Primary text
- Accent Color: #9b59b6 (Purple) - Used for special elements

**Typography:**

- Primary Font: System default sans-serif font
- Headings: Bold weight, slightly larger size
- Body Text: Regular weight, standard size
- Monospace: Used for ID fields and technical information

**Style Definitions:**

```python
# Main application style
MAIN_STYLE = """
    QWidget {
        font-family: Arial, sans-serif;
        font-size: 10pt;
        color: #333333;
    }
    QMainWindow {
        background-color: #f5f5f5;
    }
"""

# Title style
TITLE_STYLE = """
    font-size: 16pt;
    font-weight: bold;
    color: #3498db;
"""

# Card container style
CARD_STYLE = """
    background-color: white;
    border-radius: 10px;
    padding: 20px;
"""

# Button style
MAIN_BUTTON_STYLE = """
    QPushButton {
        background-color: #3498db;
        color: white;
        border-radius: 5px;
        padding: 10px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #2980b9;
    }
    QPushButton:pressed {
        background-color: #1c6ea4;
    }
"""
```

## 8. Accessibility Considerations

The UI design incorporates the following accessibility features:

1. **Keyboard Navigation**
   - All functionality accessible via keyboard
   - Tab order follows logical reading order
   - Keyboard shortcuts for common actions

2. **Visual Clarity**
   - High contrast between text and background
   - Sufficiently large text for readability
   - Visual indicators beyond color alone

3. **Screen Reader Support**
   - Alternative text for icons and images
   - Proper labeling of UI elements
   - Logical structure for screen reader traversal

4. **Input Flexibility**
   - Multiple ways to perform actions
   - Forgiving of input errors with clear correction paths
   - Clear feedback for all user actions

## 9. UI-Business Logic Integration

The UI layer integrates with the business logic through these patterns:

1. **Event-Driven Communication**
   - UI components emit signals when user actions occur
   - Business logic connects to these signals and processes data
   - Results are communicated back to UI for display

2. **Model-View Separation**
   - Data models are separate from their visual representation
   - Views update when underlying data changes
   - Business logic operates on data models, not UI components

3. **Asynchronous Processing**
   - Long-running operations run in separate threads
   - UI remains responsive during intensive processing
   - Results are synchronized back to UI thread for display

4. **Error Handling**
   - Business logic communicates errors to UI layer
   - UI presents errors in user-friendly format
   - Recovery options are offered when possible
