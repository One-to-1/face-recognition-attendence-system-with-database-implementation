# Deployment Guide

## Face Recognition Attendance System

### Table of Contents

- [Deployment Guide](#deployment-guide)
  - [Face Recognition Attendance System](#face-recognition-attendance-system)
    - [Table of Contents](#table-of-contents)
  - [1. Introduction](#1-introduction)
  - [2. System Requirements](#2-system-requirements)
    - [2.1 Hardware Requirements](#21-hardware-requirements)
    - [2.2 Software Requirements](#22-software-requirements)
  - [3. Installation](#3-installation)
    - [3.1 Python Installation](#31-python-installation)
    - [3.2 Application Installation](#32-application-installation)
      - [Option 1: Downloading from GitHub](#option-1-downloading-from-github)
      - [Option 2: Manual Download](#option-2-manual-download)
    - [3.3 Setting Up Virtual Environment](#33-setting-up-virtual-environment)
    - [3.4 Dependencies Installation](#34-dependencies-installation)
  - [4. Configuration](#4-configuration)
    - [4.1 Application Settings](#41-application-settings)
    - [4.2 Camera Setup](#42-camera-setup)
    - [4.3 Database Configuration](#43-database-configuration)
  - [5. First-Time Setup](#5-first-time-setup)
    - [5.1 Database Initialization](#51-database-initialization)
    - [5.2 Admin User Registration](#52-admin-user-registration)
    - [5.3 Initial Testing](#53-initial-testing)
  - [6. Running the Application](#6-running-the-application)
    - [6.1 Standard Startup](#61-standard-startup)
    - [6.2 Command Line Options](#62-command-line-options)
  - [7. Backup and Recovery](#7-backup-and-recovery)
    - [7.1 Database Backup](#71-database-backup)
    - [7.2 Trained Models Backup](#72-trained-models-backup)
    - [7.3 Recovery Procedures](#73-recovery-procedures)
  - [8. Troubleshooting](#8-troubleshooting)
    - [8.1 Common Issues](#81-common-issues)
    - [8.2 Logging](#82-logging)
    - [8.3 Support](#83-support)

## 1. Introduction

This deployment guide provides detailed instructions for setting up and running the Face Recognition Attendance System. The guide covers installation, configuration, operation, and troubleshooting of the application.

The Face Recognition Attendance System is designed to automate attendance tracking using facial recognition technology. It provides a user-friendly interface for registering students, capturing attendance, viewing attendance reports, and managing the database.

## 2. System Requirements

### 2.1 Hardware Requirements

- **Processor**: Intel Core i5 (7th generation or newer) or equivalent AMD processor
- **RAM**: Minimum 8GB (16GB recommended for better performance)
- **Storage**: At least 5GB of free disk space
- **Camera**: 720p webcam or higher resolution (1080p recommended)
- **Display**: 1366 x 768 resolution or higher

### 2.2 Software Requirements

- **Operating System**: Windows 10/11 (64-bit), macOS 10.15+, or Ubuntu 20.04+ (or equivalent Linux distribution)
- **Python**: Version 3.8 or higher
- **Database**: SQLite 3 (included with Python)
- **Graphics Drivers**: Up-to-date drivers for your GPU (important for face detection performance)
- **Additional Software**: Git (optional, for cloning the repository)

## 3. Installation

### 3.1 Python Installation

1. **Download Python**:
   - Visit [python.org](https://www.python.org/downloads/) and download Python 3.8 or higher.
   - Ensure you check the option "Add Python to PATH" during installation.

2. **Verify Installation**:
   - Open a command prompt or terminal.
   - Run `python --version` to verify that Python is installed correctly.
   - Run `pip --version` to verify that pip is installed correctly.

### 3.2 Application Installation

#### Option 1: Downloading from GitHub

1. **Clone the repository**:

```sh
git clone https://github.com/username/face-recognition-attendance-system.git
cd face-recognition-attendance-system
```

#### Option 2: Manual Download

1. **Download the application**:
   - Download the ZIP file from the project's GitHub page
   - Extract the ZIP file to a location of your choice

2. **Navigate to the application directory**:

   ```sh
   cd path/to/face-recognition-attendance-system
   ```

### 3.3 Setting Up Virtual Environment

It's recommended to use a virtual environment to avoid conflicts with other Python packages:

1. **Create a virtual environment**:

   ```sh
   # Windows
   python -m venv venv
   
   # macOS/Linux
   python3 -m venv venv
   ```

2. **Activate the virtual environment**:

   ```sh
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

### 3.4 Dependencies Installation

1. **Install required packages**:

   ```sh
   pip install -r requirements.txt
   ```

2. **Verify installation**:
   - Wait for all packages to be installed
   - Check for any error messages during installation

## 4. Configuration

### 4.1 Application Settings

The application settings can be configured in `config/settings.py`:

1. **Open the settings file** in a text editor:

   ```python
   # Example settings file with common options
   
   # Database path
   DB_PATH = 'facebase.db'
   
   # Data storage paths
   DATASET_DIR = 'data/dataset/'
   MODELS_DIR = 'data/models/'
   
   # Camera settings
   CAMERA_INDEX = 0  # Use 0 for default webcam
   CAMERA_RESOLUTION = (640, 480)
   
   # Face recognition settings
   CONFIDENCE_THRESHOLD = 0.7
   ```

2. **Customize the settings** according to your requirements:
   - Adjust `CAMERA_INDEX` if you have multiple cameras connected
   - Modify `CAMERA_RESOLUTION` based on your webcam's capabilities
   - Adjust `CONFIDENCE_THRESHOLD` to make recognition more/less strict

### 4.2 Camera Setup

1. **Connect the webcam** to your computer
   - Ensure it's properly recognized by your operating system

2. **Test the webcam** before starting the application:
   - On Windows, open Camera app
   - On macOS, open Photo Booth
   - On Linux, use `cheese` or another webcam application

3. **Adjust webcam position**:
   - Position the camera at eye level
   - Ensure adequate lighting for face detection
   - Avoid backlighting that can obscure faces

### 4.3 Database Configuration

The application uses SQLite, which requires minimal configuration:

1. **Database location**:
   - By default, the database file (`facebase.db`) is created in the root directory
   - You can change the path in `config/settings.py` if needed

2. **Database file permissions**:
   - Ensure the application has read and write permissions for the database file location

## 5. First-Time Setup

### 5.1 Database Initialization

The database is automatically initialized when first running the application:

1. **Run the application**:

   ```sh
   # Make sure virtual environment is activated
   python app.py
   ```

2. **Verify database creation**:
   - Check for the presence of `facebase.db` file in the root directory
   - Look for successful database initialization messages in the console

### 5.2 Admin User Registration

1. **Register the first user**:
   - Click "Register New Student" in the main window
   - Enter information in the registration form
   - Capture facial data following on-screen instructions
   - Click "Save" to register the user

### 5.3 Initial Testing

1. **Test the attendance feature**:
   - Click "Take Attendance with Camera" in the main window
   - Stand in front of the camera
   - Verify that the system recognizes the registered user
   - Check attendance record in the analytics panel

## 6. Running the Application

### 6.1 Standard Startup

1. **Navigate to the application directory**:

   ```sh
   cd path/to/face-recognition-attendance-system
   ```

2. **Activate the virtual environment** (if not already activated):

   ```sh
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Start the application**:

   ```sh
   python app.py
   ```

### 6.2 Command Line Options

The application supports several command-line options:

```sh
python app.py --help                # Display help information
python app.py --debug               # Start in debug mode with extra logging
python app.py --camera <index>      # Specify camera index to use
python app.py --reset-database      # Reset the database (warning: deletes all records)
```

## 7. Backup and Recovery

### 7.1 Database Backup

1. **Manual backup**:
   - Close the application if it's running
   - Copy the `facebase.db` file to a safe location
   - Include date information in the backup filename:

     ```sh
     cp facebase.db facebase_backup_YYYY-MM-DD.db
     ```

2. **Automated backup script**:
   - Create a script using OS-specific commands to copy the database file
   - Schedule this script to run regularly using:
     - Task Scheduler on Windows
     - Cron on macOS/Linux

### 7.2 Trained Models Backup

1. **Backup trained models**:
   - Copy the entire `data/models/` directory to a secure location:

     ```sh
     cp -r data/models/ models_backup_YYYY-MM-DD
     ```

2. **Backup face dataset**:
   - Regularly backup the `data/dataset/` directory:

     ```sh
     cp -r data/dataset/ dataset_backup_YYYY-MM-DD
     ```

### 7.3 Recovery Procedures

1. **Database recovery**:
   - Close the application if it's running
   - Replace the corrupted database file with a backup:

     ```sh
     cp facebase_backup_YYYY-MM-DD.db facebase.db
     ```

2. **Model recovery**:
   - Replace the models directory with a backup:

     ```sh
     rm -rf data/models/
     cp -r models_backup_YYYY-MM-DD data/models/
     ```

## 8. Troubleshooting

### 8.1 Common Issues

1. **Camera not detected**:
   - Verify camera connections
   - Check if another application is using the camera
   - Try changing `CAMERA_INDEX` in settings.py
   - Update camera drivers

2. **Face not recognized**:
   - Ensure adequate lighting
   - Re-register with multiple angles
   - Lower the `CONFIDENCE_THRESHOLD` in settings.py
   - Check if the model needs to be retrained

3. **Application crashes**:
   - Check log file (`app.log`) for error details
   - Ensure all dependencies are correctly installed
   - Verify Python version compatibility
   - Check system resources (memory, CPU usage)

### 8.2 Logging

The application logs its activities to help diagnose issues:

1. **Log file location**:
   - Main log file: `app.log` in the application root directory

2. **Log levels**:
   - INFO: Normal application activities
   - WARNING: Non-critical issues
   - ERROR: Critical problems that impact functionality
   - DEBUG: Detailed information (when running in debug mode)

3. **Viewing logs**:
   - Open the log file in any text editor
   - Filter for specific error types if needed

### 8.3 Support

1. **Documentation**:
   - Refer to the documentation in the `Documentation/` directory

2. **Issue reporting**:
   - Submit issues on GitHub with the following information:
     - Operating system and version
     - Python version
     - Error messages from log file
     - Steps to reproduce the problem

3. **Community support**:
   - Post questions on the project's discussion forum
   - Check existing issues for similar problems and solutions
