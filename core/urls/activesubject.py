from django.urls import path
from core.views.activesubject import (
    ActiveSubjectListView,
    ActiveSubjectCreateView,
    ActiveSubjectUpdateView,
    ActiveSubjectDeleteView,
)

app_name = "core"

urlpatterns = [
    path("activesubject/", ActiveSubjectListView.as_view(), name="activesubject_list"),
    path(
        "activesubject/create/",
        ActiveSubjectCreateView.as_view(),
        name="activesubject_create",
    ),
    path(
        "activesubject/<int:pk>/update/",
        ActiveSubjectUpdateView.as_view(),
        name="activesubject_update",
    ),
    path(
        "activesubject/<int:pk>/delete/",
        ActiveSubjectDeleteView.as_view(),
        name="activesubject_delete",
    ),
]
