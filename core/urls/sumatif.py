from django.urls import path
from core.views.sumatif import SumatifView

app_name = "core"

urlpatterns = [
    path("sumatif/", SumatifView.as_view(), name="sumatif"),
]
