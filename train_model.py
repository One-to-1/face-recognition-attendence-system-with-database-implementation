"""
Train face recognition model using KNN-based feature extraction.
This script extracts features from face images and removes the original images to save space.
"""

import cv2
import numpy as np
import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger('ModelTrainer')

# Add project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from src.core.model_training import ModelTrainer
from config.settings import DATASET_DIR, MODELS_DIR, EMBEDDINGS_PATH

def train_model():
    """Extract face features from images and build the KNN recognition model."""
    logger.info("🚀 Starting face feature extraction...")
    
    # Check if dataset directory exists
    if not os.path.exists(DATASET_DIR):
        logger.error(f"❌ Dataset directory not found: {DATASET_DIR}")
        print(f"❌ Error: Dataset directory not found at {DATASET_DIR}. Please add face images first.")
        return False
    
    # Check if there are images in the dataset
    image_count = len([f for f in os.listdir(DATASET_DIR) if os.path.isfile(os.path.join(DATASET_DIR, f))])
    if image_count == 0:
        # If no new images but we have existing features, we're good
        if os.path.exists(EMBEDDINGS_PATH):
            logger.info("✅ No new images to process, using existing features.")
            print("✅ No new images to process. Using existing face features.")
            return True
        else:
            logger.error(f"❌ No images found in dataset directory: {DATASET_DIR}")
            print(f"❌ Error: No face images found in {DATASET_DIR}. Please register users first.")
            return False
        
    # Create model trainer
    trainer = ModelTrainer()
    
    # Extract features and train the model
    logger.info(f"🔄 Processing {image_count} images from {DATASET_DIR}")
    print(f"🔄 Extracting face features from {image_count} images...")
    print("⚠️ Original images will be removed after feature extraction to save space.")
    
    success = trainer.train()
    
    if success:
        logger.info("✅ Face feature extraction completed successfully")
        print("✅ Face recognition model trained successfully!")
        return True
    else:
        logger.error("❌ Feature extraction failed")
        print("❌ Error: Feature extraction failed. Check the logs for details.")
        return False

if __name__ == "__main__":
    train_model()
