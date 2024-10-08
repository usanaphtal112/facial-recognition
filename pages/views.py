# pages/views.py
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["features"] = [
            {
                "icon": "fa-camera",
                "title": "Live Face Detection",
                "description": "Real-time face detection using your webcam.",
            },
            {
                "icon": "fa-id-badge",
                "title": "Face Recognition",
                "description": "Accurately identify and verify individuals.",
            },
            {
                "icon": "fa-upload",
                "title": "Image Upload",
                "description": "Upload images for face detection and recognition.",
            },
            {
                "icon": "fa-history",
                "title": "Detection History",
                "description": "View and manage your detection history.",
            },
        ]
        return context
