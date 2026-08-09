from django.urls import path
from core.views.backup import BackupView

app_name = "core"

urlpatterns = [
    path("config/backup/", BackupView.as_view(), name="backup"),
]
