from django.urls import path
from core.views.activeclass import (
    ActiveClassListView,
    ActiveClassCreateView,
    ActiveClassUpdateView,
    ActiveClassDeleteView,
    ActiveClassManageView,
    StudentDeleteView,
)

app_name = "core"

urlpatterns = [
    path("activeclass/", ActiveClassListView.as_view(), name="activeclass_list"),
    path(
        "activeclass/create/",
        ActiveClassCreateView.as_view(),
        name="activeclass_create",
    ),
    path(
        "activeclass/<int:pk>/update/",
        ActiveClassUpdateView.as_view(),
        name="activeclass_update",
    ),
    path(
        "activeclass/<int:pk>/delete/",
        ActiveClassDeleteView.as_view(),
        name="activeclass_delete",
    ),
    path(
        "activeclass/<int:pk>/manage/",
        ActiveClassManageView.as_view(),
        name="activeclass_manage",
    ),
    path(
        "activeclass/student/<int:pk>/delete/",
        StudentDeleteView.as_view(),
        name="activeclass_student_delete",
    ),
]
