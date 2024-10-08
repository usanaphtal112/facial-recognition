import torch
import cv2
import numpy as np
from recognition.model_architecture import FaceRecognitionModel


# Utility functions for loading model, detector paths
def get_model():
    # Load your model (the same way as in the original code)
    model_path = "E:/Machine_Learning_Project/Machine_Learning_Engineering/Model_File/face_recognizer_Rw_Eye_V1.pth"
    model = FaceRecognitionModel(embedding_size=512)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.load_state_dict(
        torch.load(model_path, map_location=device, weights_only=True)
    )
    model = model.to(device)
    return model


def get_prototxt_path():
    return "E:/Machine_Learning_Project/Machine_Learning_Engineering/Face_Recognition/Face_detection/deploy.prototxt"


def get_model_path():
    return "E:/Machine_Learning_Project/Machine_Learning_Engineering/Face_Recognition/Face_detection/res10_300x300_ssd_iter_140000.caffemodel"


def get_base_dir():
    return "F:/Datasets/Test_image/"


class FaceDetector:
    def __init__(self, prototxt_path, model_path, confidence_threshold=0.5):
        self.net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)
        self.confidence_threshold = confidence_threshold

    def detect_faces(self, frame):
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(
            cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0)
        )

        self.net.setInput(blob)
        detections = self.net.forward()

        faces = []
        for i in range(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > self.confidence_threshold:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                faces.append((startX, startY, endX - startX, endY - startY))

        return faces

    def draw_faces(self, frame, faces):
        for x, y, w, h in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        return frame
