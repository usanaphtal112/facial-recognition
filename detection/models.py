from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class DetectionRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="detections/")
    result = models.TextField()
    faces_count = models.PositiveIntegerField(default=0)
    processing_time = models.FloatField(default=0)

    def __str__(self):
        return f"Detection by {self.user} on {self.timestamp}"
