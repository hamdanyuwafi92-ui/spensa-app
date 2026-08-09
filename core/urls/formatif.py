from django.urls import path
from core.views.formatif import FormatifView

app_name = "core"

urlpatterns = [
    path("formatif/", FormatifView.as_view(), name="formatif"),
]
