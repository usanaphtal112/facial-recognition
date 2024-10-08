from django.views.generic import TemplateView, CreateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import RecognitionRecord


class RecognitionHomeView(LoginRequiredMixin, TemplateView):
    template_name = "recognition/home.html"


class LiveRecognitionView(LoginRequiredMixin, TemplateView):
    template_name = "recognition/live.html"


class ImageRecognitionView(LoginRequiredMixin, CreateView):
    model = RecognitionRecord
    fields = ["image"]
    template_name = "recognition/upload.html"
    success_url = reverse_lazy("recognition:results")

    def form_valid(self, form):
        form.instance.user = self.request.user
        # Implement face recognition logic here
        return super().form_valid(form)


class RecognitionHistoryView(LoginRequiredMixin, ListView):
    model = RecognitionRecord
    template_name = "recognition/history.html"
    context_object_name = "recognitions"
    ordering = ["-timestamp"]

    def get_queryset(self):
        return RecognitionRecord.objects.filter(user=self.request.user)


class RecognitionResultView(LoginRequiredMixin, DetailView):
    model = RecognitionRecord
    template_name = "recognition/result.html"
    context_object_name = "recognition"

    def get_queryset(self):
        return RecognitionRecord.objects.filter(user=self.request.user)
