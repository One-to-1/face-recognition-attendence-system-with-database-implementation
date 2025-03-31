"""
Configuration settings for the Face Recognition Attendance System.
"""

import os

# Base directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DATASET_DIR = os.path.join(DATA_DIR, 'dataset')
MODELS_DIR = os.path.join(DATA_DIR, 'models')

# Database settings
DB_PATH = os.path.join(BASE_DIR, 'facebase.db')

# Face recognition settings
FACE_CASCADE_PATH = "haarcascade_frontalface_default.xml"
EMBEDDINGS_PATH = os.path.join(MODELS_DIR, 'face_embeddings.pkl')
STRANGER_THRESHOLD = 0.5  # Threshold for cosine distance (0-1, lower is better match)

# Camera settings
CAMERA_INDEX = 0  # Default camera index (0 is usually the built-in webcam)

# Image capture settings
FACE_SAMPLE_COUNT = 30  # Number of face samples to capture per person