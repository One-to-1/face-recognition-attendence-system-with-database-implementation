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
MODEL_PATH = os.path.join(MODELS_DIR, 'trainer.yml')

# Image capture settings
FACE_SAMPLE_COUNT = 20  # Number of face samples to capture per person
FACE_CONFIDENCE_THRESHOLD = 70  # Threshold for face recognition confidence