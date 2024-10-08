from django.urls import path
from . import views

app_name = "recognition"

urlpatterns = [
    path("", views.RecognitionHomeView.as_view(), name="home"),
    path("live/", views.LiveRecognitionView.as_view(), name="live"),
    path("upload/", views.ImageRecognitionView.as_view(), name="upload"),
    path("history/", views.RecognitionHistoryView.as_view(), name="history"),
    path("result/<int:pk>/", views.RecognitionResultView.as_view(), name="result"),
]
