from django.urls import path
from core.views.logagent import LogAgentView

app_name = "core"

urlpatterns = [
    path("logagent/", LogAgentView.as_view(), name="logagent"),
]
