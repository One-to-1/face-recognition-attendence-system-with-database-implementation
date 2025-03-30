"""
Model training module for Face Recognition Attendance System.
Handles dataset processing and training the face recognition model.
"""

import cv2
import numpy as np
import os
import sys

# Add project root to path to allow imports from config
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from config.settings import DATASET_DIR, MODELS_DIR, MODEL_PATH

class ModelTrainer:
    def __init__(self):
        """Initialize face detector and recognizer for training."""
        self.detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
    
    def get_images_and_labels(self):
        """Process all images in dataset directory and extract faces with IDs."""
        if not os.path.exists(DATASET_DIR):
            print(f"❌ Dataset directory not found: {DATASET_DIR}")
            return [], []
            
        image_paths = [os.path.join(DATASET_DIR, f) for f in os.listdir(DATASET_DIR)]
        face_samples = []
        ids = []
        
        for image_path in image_paths:
            filename = os.path.basename(image_path)
            parts = filename.split(".")
            
            if len(parts) < 3:
                print(f"⚠️ Skipping invalid file: {filename}")
                continue
                
            try:
                id_ = int(parts[1])
                gray_img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                
                if gray_img is None:
                    print(f"⚠️ Could not read image: {image_path}")
                    continue
                    
                faces = self.detector.detectMultiScale(gray_img)
                
                for (x, y, w, h) in faces:
                    face_samples.append(gray_img[y:y+h, x:x+w])
                    ids.append(id_)
            except Exception as e:
                print(f"❌ Error processing image {image_path}: {e}")
                continue
                
        return face_samples, ids
    
    def train(self):
        """Train the face recognition model using the dataset."""
        print("🔄 Training face recognition model...")
        
        faces, ids = self.get_images_and_labels()
        
        if len(faces) == 0 or len(ids) == 0:
            print("❌ No face data found for training")
            return False
            
        print(f"🔢 Training with {len(faces)} face images")
        
        try:
            self.recognizer.train(faces, np.array(ids))
            
            # Ensure models directory exists
            if not os.path.exists(MODELS_DIR):
                os.makedirs(MODELS_DIR)
                
            self.recognizer.save(MODEL_PATH)
            print(f"✅ Model trained and saved as {MODEL_PATH}")
            return True
        except Exception as e:
            print(f"❌ Error training model: {e}")
            return False