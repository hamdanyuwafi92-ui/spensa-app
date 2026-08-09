from django.urls import path
from core.views.transcript import (
    TranscriptView,
    TranscriptDownloadView,
    TranscriptDownloadAllView,
)

app_name = "core"

urlpatterns = [
    path("transcript/", TranscriptView.as_view(), name="transcript"),
    path(
        "transcript/<int:student_id>/pdf/",
        TranscriptDownloadView.as_view(),
        name="transcript_pdf",
    ),
    path(
        "transcript/all/pdf/",
        TranscriptDownloadAllView.as_view(),
        name="transcript_all_pdf",
    ),
]
