from django.contrib import admin
from .models import DetectionRecord


@admin.register(DetectionRecord)
class DetectionRecordAdmin(admin.ModelAdmin):
    list_display = ("user", "timestamp", "faces_count", "processing_time")
    search_fields = ("user__email", "timestamp")
    list_filter = ("user", "timestamp")
    readonly_fields = ("timestamp", "faces_count", "processing_time")

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user")
