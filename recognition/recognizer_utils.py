import torch
from PIL import Image
from torchvision import transforms
import numpy as np
import os
import cv2


class FaceRecognizer:
    def __init__(self, model, base_dir):
        self.model = model
        self.base_dir = base_dir
        self.transform = transforms.Compose(
            [
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
                ),
            ]
        )

    def preprocess_image(self, image):
        image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        image = self.transform(image).unsqueeze(0)
        return image.cuda() if torch.cuda.is_available() else image

    def get_image_paths(self):
        image_paths = []
        for root, dirs, files in os.walk(self.base_dir):
            for file in files:
                if file.endswith((".jpg", ".png")):
                    image_paths.append(os.path.join(root, file))
        return image_paths

    def recognize_face(self, input_image):
        self.model.eval()
        with torch.no_grad():
            input_embedding = self.model(input_image).cpu().numpy()

        base_images = self.get_image_paths()
        best_match = None
        best_distance = float("inf")

        for base_image_path in base_images:
            base_image = self.preprocess_image(cv2.imread(base_image_path))
            with torch.no_grad():
                base_embedding = self.model(base_image).cpu().numpy()

            distance = np.linalg.norm(input_embedding - base_embedding)
            if distance < best_distance:
                best_distance = distance
                best_match = base_image_path

        if best_distance > 0.2:
            return "Unknown", best_distance
        else:
            return os.path.basename(os.path.dirname(best_match)), best_distance
