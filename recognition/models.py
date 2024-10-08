from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class RecognitionRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="recognitions/")
    recognized_name = models.CharField(max_length=100)
    confidence_score = models.FloatField()
