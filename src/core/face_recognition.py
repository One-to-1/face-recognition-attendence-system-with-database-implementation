"""
Face recognition module for the Face Recognition Attendance System.
Handles face detection and recognition using KNN-based approach.
"""

import cv2
import numpy as np
import os
import sys
import pickle
from sklearn.preprocessing import Normalizer
from sklearn.neighbors import KNeighborsClassifier

# Add project root to path to allow imports from config
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from config.settings import FACE_CASCADE_PATH, EMBEDDINGS_PATH, STRANGER_THRESHOLD

class FaceRecognizer:
    def __init__(self):
        """Initialize face detector and recognizer."""
        # For face detection
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + FACE_CASCADE_PATH)
        
        # For advanced recognition using local features
        self.knn_model = None
        self.feature_dict = {}
        self.l2_normalizer = Normalizer('l2')
        
        # Initialize models
        self.initialize_models()
        
    def initialize_models(self):
        """Load trained face recognition models."""
        try:
            # Load feature dictionary for KNN recognition
            if os.path.exists(EMBEDDINGS_PATH):
                with open(EMBEDDINGS_PATH, 'rb') as f:
                    self.feature_dict = pickle.load(f)
                print(f"✅ Face features loaded from {EMBEDDINGS_PATH}")
                
                # Create KNN model from the features
                if self.feature_dict:
                    self.create_knn_model()
            else:
                print(f"❗ Face features not found at {EMBEDDINGS_PATH}")
                
        except Exception as e:
            print(f"❌ Error loading models: {e}")
    
    def create_knn_model(self):
        """Create a KNN model from the stored face features."""
        try:
            features = []
            labels = []
            
            for user_id, user_features in self.feature_dict.items():
                for feature in user_features:
                    features.append(feature)
                    labels.append(user_id)
            
            if len(features) > 0:
                self.knn_model = KNeighborsClassifier(n_neighbors=1, metric='cosine')
                self.knn_model.fit(features, labels)
                print(f"✅ KNN model created with {len(features)} features")
        except Exception as e:
            print(f"❌ Error creating KNN model: {e}")
            self.knn_model = None
    
    def detect_faces(self, frame):
        """Detect faces in a frame and return face regions."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        face_regions = []
        
        for (x, y, w, h) in faces:
            # Get both grayscale and color versions of the face
            gray_face = gray[y:y+h, x:x+w]
            color_face = frame[y:y+h, x:x+w]
            face_regions.append((x, y, w, h, gray_face, color_face))
            
        return face_regions
    
    def extract_face_features(self, face_img):
        """Extract features from a face image for enhanced recognition."""
        try:
            # Resize for consistency
            face = cv2.resize(face_img, (100, 100))
            
            # Calculate histograms in different regions
            features = []
            h, w = face.shape[:2]
            
            # Convert to grayscale if not already
            if len(face.shape) > 2:
                gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
            else:
                gray = face
                
            # Calculate histograms for different face regions
            regions = [(0, 0, w//2, h//2), (w//2, 0, w//2, h//2), 
                      (0, h//2, w//2, h//2), (w//2, h//2, w//2, h//2)]
            
            for (x, y, rw, rh) in regions:
                roi = gray[y:y+rh, x:x+rw]
                hist = cv2.calcHist([roi], [0], None, [16], [0, 256])
                hist = cv2.normalize(hist, hist).flatten()
                features.extend(hist)
            
            # Add LBPH-like features
            lbp = self.get_lbp_features(gray)
            features.extend(lbp)
            
            # Normalize the feature vector
            features = np.array(features)
            features = self.l2_normalizer.transform([features])[0]
            
            return features
            
        except Exception as e:
            print(f"❌ Error extracting face features: {e}")
            return None
    
    def get_lbp_features(self, gray_img):
        """Extract LBP-like features manually."""
        h, w = gray_img.shape
        lbp_features = []
        
        # Calculate simple gradient features in different directions
        for i in range(1, h-1, 4):
            for j in range(1, w-1, 4):
                # Get the 3x3 neighborhood
                patch = gray_img[i-1:i+2, j-1:j+2]
                center = patch[1, 1]
                # Calculate gradient magnitudes
                dx = abs(int(patch[1, 2]) - int(patch[1, 0]))
                dy = abs(int(patch[2, 1]) - int(patch[0, 1]))
                diag1 = abs(int(patch[2, 2]) - int(patch[0, 0]))
                diag2 = abs(int(patch[2, 0]) - int(patch[0, 2]))
                
                lbp_features.extend([dx, dy, diag1, diag2])
        
        return lbp_features
    
    def recognize_face(self, gray_face, color_face):
        """Recognize a face and return ID and confidence."""
        try:
            # Check if KNN model is available
            if self.knn_model is None:
                return None, 0, False
                
            # Extract features from the face
            face_features = self.extract_face_features(color_face)
            if face_features is None:
                return None, 0, False
                
            # Get prediction from the KNN model
            user_id = self.knn_model.predict([face_features])[0]
            # Get distance to the nearest neighbor
            distances, _ = self.knn_model.kneighbors([face_features])
            distance = distances[0][0]
            
            # Check if the distance is below the threshold
            if distance < STRANGER_THRESHOLD:
                # Convert distance to confidence score (0-100)
                confidence = (1 - distance) * 100
                return str(user_id), confidence, True
            else:
                # This is a stranger
                return None, (1 - distance) * 100, False
            
        except Exception as e:
            print(f"❌ Error recognizing face: {e}")
            return None, 0, False
            
    def draw_face_box(self, frame, x, y, w, h, label, is_stranger=False):
        """Draw box around face with label."""
        # Use red for strangers, blue for known faces
        color = (0, 0, 255) if is_stranger else (255, 0, 0)
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        
        # Add a background to the label for better visibility
        label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)
        cv2.rectangle(frame, (x, y-label_size[1]-10), (x+label_size[0], y), color, cv2.FILLED)
        cv2.putText(frame, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        # Add a warning icon for strangers
        if is_stranger:
            warning_text = "⚠️ STRANGER"
            cv2.putText(frame, warning_text, (x, y+h+25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            
        return frame