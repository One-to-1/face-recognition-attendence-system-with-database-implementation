# Deployment Guide

## Overview

This document provides instructions for deploying the Face Recognition Attendance System. It includes system requirements, installation steps, configuration options, and troubleshooting guidelines.

## System Requirements

### Hardware Requirements

- **Processor**: Intel Core i3 or equivalent (i5 or higher recommended)
- **RAM**: 4GB minimum (8GB or higher recommended)
- **Storage**: 500MB for application, plus additional space for database and face datasets
- **Camera**: Webcam with minimum 720p resolution
- **Display**: 1280×720 minimum resolution

### Software Requirements

- **Operating System**: Windows 10/11, macOS 10.15+, or Ubuntu 20.04+ (Windows recommended)
- **Python**: Version 3.8 or higher
- **Required Libraries**: See `requirements.txt` file for detailed dependencies

## Installation Steps

### 1. Clone or Download the Repository

```bash
git clone https://github.com/yourusername/face-recognition-attendence-system-with-database-implementation.git
cd face-recognition-attendence-system-with-database-implementation
```

### 2. Set Up a Python Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Initialize the Database

```bash
python app.py --init-db
```

### 5. Run the Application

```bash
python app.py
```

## Configuration Options

The system can be configured by modifying the settings in `config/settings.py`.

### Key Configuration Options

#### Database Settings

```python
# Database file path
DB_PATH = os.path.join(BASE_DIR, 'facebase.db')
```

#### Face Recognition Settings

```python
# Path to the face cascade classifier
FACE_CASCADE_PATH = "haarcascade_frontalface_default.xml"

# Path to the face embeddings model
EMBEDDINGS_PATH = os.path.join(MODELS_DIR, 'face_embeddings.pkl')

# Threshold for face recognition confidence (lower = stricter matching)
STRANGER_THRESHOLD = 0.5
```

#### Image Capture Settings

```python
# Number of face samples to capture per person during registration
FACE_SAMPLE_COUNT = 20
```

## Directory Structure Overview

```txt
project/
│
├── app.py                  # Main application entry point
├── train_model.py          # Standalone script to train the model
├── requirements.txt        # Python dependencies
├── facebase.db             # SQLite database file (created on first run)
│
├── config/                 # Configuration settings
│   └── settings.py
│
├── data/                   # Data storage
│   ├── dataset/            # Captured face images stored here
│   └── models/             # Trained face recognition models
│       └── face_embeddings.pkl
│
└── src/                    # Application source code
    ├── core/               # Core functionality
    │   ├── attendance.py
    │   ├── face_recognition.py
    │   └── model_training.py
    │
    ├── database/           # Database operations
    │   ├── db_manager.py
    │   └── schema.py
    │
    ├── ui/                 # User interface components
    │   ├── main_window.py
    │   └── ...
    │
    └── utils/              # Utility functions
        ├── image_utils.py
        └── validation.py
```

## Running the System

### Registration Mode

To register new users:

1. Launch the application: `python app.py`
2. Click "Register New Student" on the main window
3. Enter user details and capture face samples
4. Save the user record

### Attendance Mode

To mark attendance:

1. Launch the application: `python app.py`
2. Click "Take Attendance with Camera" on the main window
3. The system will automatically detect and recognize faces
4. Attendance is recorded automatically for recognized individuals

### Analytics Mode

To view attendance reports:

1. Launch the application: `python app.py`
2. Click "View Attendance Reports" on the main window
3. Select the desired report type and date range
4. Export reports as needed

## Command Line Arguments

The application supports the following command line arguments:

- `--init-db`: Initialize or reset the database
- `--train-model`: Force retraining of the face recognition model
- `--debug`: Run in debug mode with additional logging
- `--help`: Show help message

Example:

```bash
python app.py --debug
```

## Training the Model

The face recognition model is trained automatically when new users are registered. However, you can force a complete retraining of the model:

```bash
python train_model.py
```

or

```bash
python app.py --train-model
```

## Database Management

### Backup Database

To backup the SQLite database:

```bash
cp facebase.db facebase.db.backup
```

### Restore Database

To restore from a backup:

```bash
cp facebase.db.backup facebase.db
```

### Reset Database

To reset the database (warning: this will delete all data):

```bash
python app.py --init-db
```

## Troubleshooting

### Camera Issues

- **Problem**: Camera not detected
  - **Solution**: Ensure the camera is properly connected and not in use by another application
  - **Solution**: Try changing the camera index in the code if you have multiple cameras

- **Problem**: Poor face detection
  - **Solution**: Improve lighting conditions
  - **Solution**: Adjust the face detection parameters in the code

### Recognition Issues

- **Problem**: Poor face recognition accuracy
  - **Solution**: Retrain the model with more samples per person
  - **Solution**: Adjust the `STRANGER_THRESHOLD` in settings.py
  - **Solution**: Ensure lighting conditions are similar between registration and attendance

### Database Issues

- **Problem**: Database errors
  - **Solution**: Check file permissions
  - **Solution**: Run the application with admin/sudo privileges
  - **Solution**: Restore from a backup if database is corrupted

### Application Crashes

- **Problem**: Application crashes on startup
  - **Solution**: Check that all dependencies are installed correctly
  - **Solution**: Verify Python version compatibility
  - **Solution**: Check the app.log file for detailed error information

## Logging

The application writes logs to `app.log` in the root directory. For troubleshooting, check this file for error messages and warnings.

## Security Considerations

1. **Database Security**:
   - The SQLite database file should have appropriate file permissions
   - For production use, consider using a more robust database system

2. **Image Storage**:
   - Face images are stored locally in the data/dataset directory
   - Ensure appropriate file system permissions to protect privacy

3. **User Privacy**:
   - The system stores biometric data (face embeddings)
   - Ensure compliance with relevant privacy regulations
   - Consider implementing data retention policies

## Performance Optimization

1. **Hardware Acceleration**:
   - If available, the system can use GPU acceleration for face recognition
   - Install appropriate CUDA libraries if using NVIDIA graphics cards

2. **Large Deployments**:
   - For larger installations, consider:
     - Moving to a client-server architecture
     - Using a more robust database like PostgreSQL
     - Implementing load balancing for multiple camera feeds

## Updating the System

To update the system when new versions are available:

1. Backup the database and face embeddings
2. Pull the latest code from the repository
3. Install any new dependencies
4. Run the application with the existing database

## Support and Resources

For additional help and resources:

- Submit issues on the GitHub repository
- Consult the documentation in the design directory
- Refer to library documentation for dependencies (OpenCV, PyQt5, etc.)
