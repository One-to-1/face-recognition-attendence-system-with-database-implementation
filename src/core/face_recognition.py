"""
Face recognition module for the Face Recognition Attendance System.
Handles face detection and recognition.
"""

import cv2
import numpy as np
import os
import sys

# Add project root to path to allow imports from config
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from config.settings import FACE_CASCADE_PATH, MODEL_PATH, FACE_CONFIDENCE_THRESHOLD

class FaceRecognizer:
    def __init__(self):
        """Initialize face detector and recognizer."""
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + FACE_CASCADE_PATH)
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.load_model()
    
    def load_model(self):
        """Load trained face recognition model."""
        try:
            if os.path.exists(MODEL_PATH):
                self.recognizer.read(MODEL_PATH)
                print(f"✅ Model loaded from {MODEL_PATH}")
            else:
                print(f"❗ Model file not found at {MODEL_PATH}")
        except Exception as e:
            print(f"❌ Error loading model: {e}")
    
    def detect_faces(self, frame):
        """Detect faces in a frame and return face regions."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        face_regions = []
        
        for (x, y, w, h) in faces:
            face_regions.append((x, y, w, h, gray[y:y+h, x:x+w]))
            
        return face_regions
    
    def recognize_face(self, face_img):
        """Recognize a face and return ID and confidence."""
        try:
            id_, confidence = self.recognizer.predict(face_img)
            if confidence < FACE_CONFIDENCE_THRESHOLD:
                return str(id_), confidence
            return None, confidence
        except Exception as e:
            print(f"❌ Error recognizing face: {e}")
            return None, 100
            
    def draw_face_box(self, frame, x, y, w, h, label):
        """Draw box around face with label."""
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.putText(frame, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        return frame