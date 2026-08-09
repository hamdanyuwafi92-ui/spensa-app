from django.urls import path
from core.views.report import ReportView

app_name = "core"

urlpatterns = [
    path("report/", ReportView.as_view(), name="report"),
]
