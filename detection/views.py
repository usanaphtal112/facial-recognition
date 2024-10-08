from django.views.generic import TemplateView, CreateView, ListView, DetailView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import DetectionRecord
from django.urls import reverse_lazy
from .detector_utils import (
    FaceDetector,
    get_model_path,
    get_prototxt_path,
)
from django.http import JsonResponse
import cv2
import numpy as np
from PIL import Image
from io import BytesIO
import time
import base64

face_detector = FaceDetector(get_prototxt_path(), get_model_path())


class DetectionHomeView(LoginRequiredMixin, TemplateView):
    template_name = "detection/home.html"


class ImageFaceDetectionView(LoginRequiredMixin, CreateView):
    model = DetectionRecord
    fields = ["image"]
    template_name = "detection/upload.html"

    def form_valid(self, form):
        form.instance.user = self.request.user

        # Get the uploaded image
        uploaded_file = self.request.FILES["image"]

        # Read the image from the uploaded file
        image_data = uploaded_file.read()
        image_stream = BytesIO(image_data)
        image = Image.open(image_stream)

        # Convert PIL image to OpenCV format
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        # Detect faces
        face_detector = FaceDetector(get_prototxt_path(), get_model_path())
        faces = face_detector.detect_faces(image)

        # Save the detection result in the form
        form.instance.result = f"Detected {len(faces)} faces"
        form.instance.detection_data = str(faces)  # Store face coordinates

        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to the detection result page after the form is successfully submitted
        return reverse_lazy("detection:results", kwargs={"pk": self.object.pk})


class DetectionHistoryView(LoginRequiredMixin, ListView):
    model = DetectionRecord
    template_name = "detection/history.html"
    context_object_name = "detections"
    ordering = ["-timestamp"]

    def get_queryset(self):
        return DetectionRecord.objects.filter(user=self.request.user)


class DetectionResultView(LoginRequiredMixin, DetailView):
    model = DetectionRecord
    template_name = "detection/result.html"
    context_object_name = "detection"

    def get_queryset(self):
        return DetectionRecord.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        detection_record = self.get_object()

        # Load the saved image
        image_path = detection_record.image.path
        image = cv2.imread(image_path)

        # Start timer to calculate processing time
        start_time = time.time()

        # Initialize the face detector
        face_detector = FaceDetector(get_prototxt_path(), get_model_path())

        # Detect faces
        faces = face_detector.detect_faces(image)
        detection_record.faces_count = len(faces)

        # Draw rectangles around the faces
        for x, y, w, h in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Calculate processing time
        processing_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        detection_record.processing_time = processing_time
        detection_record.save()

        # Convert image to display in template
        is_success, buffer = cv2.imencode(".jpg", image)
        processed_image = buffer.tobytes()
        img_b64 = "data:image/jpeg;base64," + base64.b64encode(processed_image).decode()

        # Add detection details to context
        context["processed_image"] = img_b64
        context["faces"] = [
            {"x": x, "y": y, "width": w, "height": h} for (x, y, w, h) in faces
        ]
        context["processing_time"] = processing_time

        return context


class LiveDetectionView(LoginRequiredMixin, TemplateView):
    template_name = "detection/live_detection.html"


class ProcessFrameView(View):
    def post(self, request, *args, **kwargs):
        try:
            print("Received frame processing request")  # Direct print for debugging

            if request.FILES.get("frame"):
                frame_file = request.FILES["frame"]
                print(
                    f"Frame file size: {frame_file.size} bytes"
                )  # Direct print for debugging

                frame_data = np.frombuffer(frame_file.read(), np.uint8)
                frame = cv2.imdecode(frame_data, cv2.IMREAD_COLOR)
                print(
                    f"Decoded frame shape: {frame.shape}"
                )  # Direct print for debugging

                faces = face_detector.detect_faces(frame)
                print(
                    f"Detected {len(faces)} faces: {faces}"
                )  # Direct print for debugging

                results = [
                    {"x": int(x), "y": int(y), "width": int(w), "height": int(h)}
                    for (x, y, w, h) in faces
                ]

                print(f"Returning results: {results}")  # Direct print for debugging
                return JsonResponse({"faces": results})

            print("No frame provided in request")  # Direct print for debugging
            return JsonResponse({"error": "No frame provided"}, status=400)
        except Exception as e:
            print(f"Error processing frame: {str(e)}")  # Direct print for debugging
            return JsonResponse({"error": str(e)}, status=500)
