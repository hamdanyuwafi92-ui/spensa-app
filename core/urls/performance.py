from django.urls import path
from core.views.performance import PerformanceView

app_name = "core"

urlpatterns = [
    path("performance/", PerformanceView.as_view(), name="performance"),
]
