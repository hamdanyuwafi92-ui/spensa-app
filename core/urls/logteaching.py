from django.urls import path
from core.views.logteaching import LogTeachingView

app_name = "core"

urlpatterns = [
    path("logteaching/", LogTeachingView.as_view(), name="logteaching"),
]
