"""
Model training module for Face Recognition Attendance System.
Handles processing of face data and extraction of features for KNN-based recognition.
"""

import cv2
import numpy as np
import os
import sys
import pickle
import shutil
from sklearn.preprocessing import Normalizer
from tqdm import tqdm

# Add project root to path to allow imports from config
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from config.settings import DATASET_DIR, MODELS_DIR, EMBEDDINGS_PATH

class ModelTrainer:
    def __init__(self):
        """Initialize face detector and feature extractor for training."""
        self.detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        self.l2_normalizer = Normalizer('l2')
        
        # Ensure models directory exists
        if not os.path.exists(MODELS_DIR):
            os.makedirs(MODELS_DIR)
    
    def extract_face_features(self, face_img):
        """Extract features from a face image for recognition."""
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
    
    def process_images_and_extract_features(self):
        """Process images in the dataset directory, extract features, and then remove the images."""
        print("🔄 Processing images and extracting features...")
        
        if not os.path.exists(DATASET_DIR):
            print(f"❌ Dataset directory not found: {DATASET_DIR}")
            return None
            
        image_paths = [os.path.join(DATASET_DIR, f) for f in os.listdir(DATASET_DIR) 
                      if os.path.isfile(os.path.join(DATASET_DIR, f))]
        
        if not image_paths:
            print("❌ No images found in dataset directory!")
            return None
            
        # Load existing features if available
        feature_dict = {}
        if os.path.exists(EMBEDDINGS_PATH):
            try:
                with open(EMBEDDINGS_PATH, 'rb') as f:
                    feature_dict = pickle.load(f)
                print(f"✅ Loaded existing features from {EMBEDDINGS_PATH}")
            except Exception as e:
                print(f"⚠️ Could not load existing features: {e}")
        
        # Track processed files for deletion later
        processed_files = []
        
        for image_path in tqdm(image_paths, desc="Extracting Features"):
            # Load the image
            img = cv2.imread(image_path)
            if img is None:
                print(f"⚠️ Could not read image: {image_path}")
                continue
                
            # Extract ID from filename
            try:
                id_ = str(os.path.split(image_path)[-1].split(".")[1])
            except (IndexError, ValueError):
                print(f"⚠️ Invalid filename format: {image_path}")
                continue
                
            # Detect faces in the image
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.detector.detectMultiScale(gray)
            
            if len(faces) != 1:
                print(f"⚠️ Image {image_path} has {len(faces)} faces, expected 1")
                continue
                
            # Extract the face region and compute features
            for (x, y, w, h) in faces:
                face_img = img[y:y+h, x:x+w]
                features = self.extract_face_features(face_img)
                
                if features is not None:
                    if id_ not in feature_dict:
                        feature_dict[id_] = []
                    feature_dict[id_].append(features)
                    processed_files.append(image_path)
        
        # Remove processed images
        if processed_files:
            for file_path in processed_files:
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f"⚠️ Could not remove file {file_path}: {e}")
            
            print(f"✅ Removed {len(processed_files)} processed images to save space")
                    
        return feature_dict

    def train(self):
        """Extract features from faces, build the KNN model, and save the features."""
        print("🔄 Training face recognition model...")
        
        # Process images, extract features, and remove them
        feature_dict = self.process_images_and_extract_features()
        
        if feature_dict is None or len(feature_dict) == 0:
            print("❌ No face features extracted")
            return False
            
        # Save the extracted features
        try:
            with open(EMBEDDINGS_PATH, 'wb') as f:
                pickle.dump(feature_dict, f)
            print(f"✅ Face features saved to {EMBEDDINGS_PATH}")
            
            # Display summary
            total_features = sum(len(feat) for feat in feature_dict.values())
            print(f"📊 Generated features for {len(feature_dict)} users with {total_features} total face samples")
            
            return True
        except Exception as e:
            print(f"❌ Error saving face features: {e}")
            return False