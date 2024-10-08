from django.urls import path
from . import views

app_name = "detection"

urlpatterns = [
    path("", views.DetectionHomeView.as_view(), name="home"),
    path("live/", views.LiveDetectionView.as_view(), name="live_detection"),
    path("process-frame/", views.ProcessFrameView.as_view(), name="process_frame"),
    path("upload/", views.ImageFaceDetectionView.as_view(), name="upload"),
    path("history/", views.DetectionHistoryView.as_view(), name="history"),
    path("result/<int:pk>/", views.DetectionResultView.as_view(), name="results"),
]
