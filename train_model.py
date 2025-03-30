import cv2
import numpy as np
import os

def train_model():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    def get_images_and_labels(path):
        image_paths = [os.path.join(path, f) for f in os.listdir(path)]
        face_samples = []
        ids = []
        for imagePath in image_paths:
            gray_img = cv2.imread(imagePath, cv2.IMREAD_GRAYSCALE)
            id_ = int(os.path.split(imagePath)[-1].split(".")[1])
            faces = detector.detectMultiScale(gray_img)
            for (x, y, w, h) in faces:
                face_samples.append(gray_img[y:y+h, x:x+w])
                ids.append(id_)
        return face_samples, ids

    faces, ids = get_images_and_labels("dataset")
    recognizer.train(faces, np.array(ids))
    recognizer.save("trainer/trainer.yml")
    print("✅ Model trained and saved as trainer/trainer.yml")

if __name__ == "__main__":
    train_model()
