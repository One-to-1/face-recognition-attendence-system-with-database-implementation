"""
Main entry point for the Face Recognition Attendance System application.
"""

import sys
import os
from PyQt5.QtWidgets import QApplication
import logging
import codecs

# Fix Windows console encoding issues - can handle Unicode characters including emojis
if sys.platform == 'win32':
    # Force UTF-8 encoding for stdout/stderr
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

# Import main window
from src.ui.main_window import MainWindow

# Import settings
from config.settings import DATASET_DIR, MODELS_DIR

def setup_directories():
    """Create required directories if they don't exist."""
    dirs = [DATASET_DIR, MODELS_DIR]
    for dir_path in dirs:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            logger.info(f"Created directory: {dir_path}")

def main():
    """Main application entry point."""
    # Set up directories
    setup_directories()
    
    # Start PyQt application
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    
    logger.info("Application started successfully")
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()