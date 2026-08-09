from django.urls import path
from core.views.loglearning import LogLearningListView, LogLearningDetailView

app_name = "core"

urlpatterns = [
    path("loglearning/", LogLearningListView.as_view(), name="loglearning_list"),
    path(
        "loglearning/detail/",
        LogLearningDetailView.as_view(),
        name="loglearning_detail",
    ),
]
