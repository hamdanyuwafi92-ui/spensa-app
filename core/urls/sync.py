from django.urls import path
from core.views.sync import SyncView

app_name = "core"

urlpatterns = [
    path("settings/", SyncView.as_view(), name="sync"),
]
