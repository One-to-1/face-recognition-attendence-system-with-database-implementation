# UI/UX Design Specifications

## Overview

This document outlines the user interface and user experience design for the Face Recognition Attendance System. The system uses PyQt5 to create a modern, intuitive interface that guides users through registration, attendance capture, and analytics processes.

## Design Principles

The UI design of the application follows these key principles:

1. **Simplicity**: Clean, uncluttered interfaces that focus on the task at hand
2. **Consistency**: Uniform styling, spacing, and interaction patterns throughout the application
3. **Feedback**: Clear visual and textual feedback for user actions
4. **Accessibility**: Adequate contrast, readable fonts, and accommodating UI elements
5. **Error Prevention**: Validation and confirmation to prevent user errors

## Color Scheme

The application uses a consistent color palette throughout:

- **Primary Color**: #3498db (Blue) - Used for buttons, headers, and interactive elements
- **Secondary Color**: #2c3e50 (Dark Blue) - Used for text and minor UI elements
- **Background Color**: #f5f5f5 (Light Gray) - Main background color
- **Accent Colors**:
  - Success: #27ae60 (Green) - For success messages and confirmed actions
  - Warning: #f39c12 (Orange) - For warnings and cautions
  - Error: #e74c3c (Red) - For error messages and alerts
  - Neutral: #95a5a6 (Gray) - For disabled elements and secondary text

## Typography

- **Primary Font**: System default sans-serif font (for cross-platform compatibility)
- **Title Size**: 18-24pt (bold)
- **Subtitle Size**: 14-16pt (semi-bold)
- **Body Text Size**: 10-12pt (regular)
- **Button Text**: 12pt (semi-bold)

## Screen Flow Diagram

```txt
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  Main Window    │────►│Register Window  │────►│ Camera Capture  │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                                               │
        │                                               │
        ▼                                               ▼
┌─────────────────┐                            ┌─────────────────┐
│                 │                            │                 │
│Analytics Window │                            │Attendance Window│
│                 │                            │                 │
└─────────────────┘                            └─────────────────┘
        │                                               │
        │                                               │
        ▼                                               ▼
┌─────────────────┐                            ┌─────────────────┐
│                 │                            │                 │
│Export Reports   │                            │Recognition      │
│                 │                            │Feedback         │
└─────────────────┘                            └─────────────────┘
```

## Screen Specifications

### Main Window

![Main Window Wireframe]

**Key Elements:**

- Application title and logo
- Three main action buttons with icons:
  - Register New Student
  - Take Attendance with Camera
  - View Attendance Reports
- Footer with application information

**Layout:**

- Vertical layout with centered elements
- Card container for main content
- Fixed minimum window size (640x480)
- Responsive resizing for larger displays

**Interactions:**

- Button hover effects for clear feedback
- Each button opens its respective window
- Window is centered on screen when launched

### Register Window

![Register Window Wireframe]

**Key Elements:**

- Input fields:
  - Student ID (with validation)
  - Full Name (with validation)
- Camera preview area
- Capture button
- Status indicator
- Save/Cancel buttons

**Layout:**

- Two-column layout (form fields and camera preview)
- Status messages below camera preview
- Bottom-aligned action buttons

**Interactions:**

- Real-time input validation with error messages
- Camera preview updates continuously
- Capture button takes multiple face samples
- Visual progress indicator during capture
- Success/failure feedback after registration attempt

### Attendance Window

![Attendance Window Wireframe]

**Key Elements:**

- Large camera feed display
- Recognition status panel
- Recently recognized user list
- Date and time display
- Start/Stop attendance capture button

**Layout:**

- Camera feed occupies majority of window space
- Status panel on the right side
- Controls at the bottom

**Interactions:**

- Faces in camera feed are highlighted with bounding boxes
- Different box colors for recognized vs. unrecognized faces
- Real-time feedback when a face is recognized
- Attendance confirmation message appears briefly
- Recently recognized names appear in a scrollable list

### Analytics Window

![Analytics Window Wireframe]

**Key Elements:**

- Date range selector
- Report type selector (daily, monthly, per student)
- Data visualization area
- Data table with attendance information
- Export button

**Layout:**

- Controls at the top
- Visualization below controls (when applicable)
- Scrollable data table taking majority of space
- Export button at the bottom

**Interactions:**

- Date selector updates report automatically
- Sorting options for table columns
- Search/filter functionality for large datasets
- Export options for different file formats

## UI Components & Styling

### Buttons

```css
QPushButton {
    background-color: #3498db;
    border: none;
    color: white;
    padding: 8px 16px;
    border-radius: 4px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #2980b9;
}

QPushButton:disabled {
    background-color: #95a5a6;
}
```

### Input Fields

```css
QLineEdit {
    padding: 8px;
    border: 1px solid #dcdde1;
    border-radius: 4px;
}

QLineEdit:focus {
    border: 2px solid #3498db;
}

QLineEdit[invalid="true"] {
    border: 2px solid #e74c3c;
}
```

### Labels

```css
QLabel {
    color: #2c3e50;
}

QLabel.title {
    font-size: 20pt;
    font-weight: bold;
    color: #2c3e50;
}

QLabel.subtitle {
    font-size: 14pt;
    color: #34495e;
}
```

### Tables

```css
QTableWidget {
    border: 1px solid #dcdde1;
    gridline-color: #ecf0f1;
}

QTableWidget::item {
    padding: 4px;
}

QHeaderView::section {
    background-color: #f5f5f5;
    padding: 4px;
    font-weight: bold;
    border: 1px solid #dcdde1;
}
```

## Icons

The application uses a consistent icon set for better visual communication:

- **User Plus Icon**: For registration functionality
- **Camera Icon**: For attendance capture
- **Chart Icon**: For analytics and reports
- **Check Icon**: For confirmation/success feedback
- **X Icon**: For errors/cancellation
- **Export Icon**: For report export functionality

Icons are stored in the `src/ui/icons/` directory and loaded via the `icons.py` utility module.

## Responsive Design Considerations

The UI is designed to be responsive within these constraints:

- Minimum window size enforced to prevent layout issues
- Elements use proportional sizing where appropriate
- Table views and lists are scrollable for varying content amounts
- Window layouts adjust for different screen resolutions

## Accessibility Considerations

- Keyboard navigation supported for all interactive elements
- Adequate color contrast for text readability
- Error messages are both visual and text-based
- Icons are paired with text labels for clarity

## Error Handling UI

- Input validation errors appear as:
  - Red border on the invalid field
  - Tooltip or inline error message
  - Disabled submit button until errors are resolved
- System errors displayed in a modal dialog with:
  - Clear error message
  - Possible solutions or next steps
  - Option to report the error

## UI Performance Considerations

- Camera feed rendering is optimized to reduce CPU usage
- Large datasets in analytics view use pagination
- Background operations indicate progress visually
- Resource-intensive operations run in separate threads to keep UI responsive

## User Flow for Key Tasks

### User Registration Flow

1. Open main window
2. Click "Register New Student"
3. Enter student ID and name
4. Click "Start Camera" to initialize camera
5. Position face in frame and click "Capture"
6. System captures multiple face samples
7. Click "Save" to complete registration
8. System shows success confirmation

### Attendance Marking Flow

1. Open main window
2. Click "Take Attendance with Camera"
3. Camera activates automatically
4. Students position face in camera view
5. System recognizes face and displays name
6. Attendance is marked automatically
7. Student receives confirmation
8. Process repeats for next student

### Viewing Reports Flow

1. Open main window
2. Click "View Attendance Reports"
3. Select report type
4. Choose date range
5. View generated report
6. (Optional) Export report to file
