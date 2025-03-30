"""
Image utility functions for Face Recognition Attendance System.
"""
import cv2
import numpy as np
import os

def resize_image(image, width=None, height=None):
    """
    Resize an image while maintaining aspect ratio.
    Specify either width or height, the other will be calculated.
    """
    if width is None and height is None:
        return image
        
    (h, w) = image.shape[:2]
    
    if width is None:
        ratio = height / float(h)
        dim = (int(w * ratio), height)
    else:
        ratio = width / float(w)
        dim = (width, int(h * ratio))
    
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    return resized

def normalize_image(image):
    """
    Normalize image brightness and contrast.
    """
    # Convert to LAB color space
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    
    # Apply CLAHE to L-channel
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    
    # Merge the CLAHE enhanced L-channel with the a and b channels
    limg = cv2.merge((cl, a, b))
    
    # Convert back to BGR color space
    enhanced = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    return enhanced

def crop_face(image, face_coords):
    """
    Crop a face from an image based on coordinates.
    face_coords: tuple (x, y, w, h)
    """
    x, y, w, h = face_coords
    return image[y:y+h, x:x+w]

def draw_face_box(image, face_coords, label=None, color=(0, 255, 0), thickness=2):
    """
    Draw a box around a face with an optional label.
    """
    x, y, w, h = face_coords
    cv2.rectangle(image, (x, y), (x+w, y+h), color, thickness)
    
    if label:
        # Draw label background
        cv2.rectangle(image, (x, y-30), (x+w, y), color, -1)
        # Draw label text
        cv2.putText(image, label, (x+5, y-10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    
    return image