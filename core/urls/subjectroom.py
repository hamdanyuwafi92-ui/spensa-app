from django.urls import path
from core.views.subjectroom import (
    SubjectRoomManageView,
    ClassroomCreateView,
    ClassroomUpdateView,
    ClassroomDeleteView,
    SubjectCreateView,
    SubjectUpdateView,
    SubjectDeleteView,
)

app_name = "core"

urlpatterns = [
    path("subjectroom/", SubjectRoomManageView.as_view(), name="subjectroom_manage"),
    path(
        "subjectroom/classroom/create/",
        ClassroomCreateView.as_view(),
        name="classroom_create",
    ),
    path(
        "subjectroom/classroom/<int:pk>/update/",
        ClassroomUpdateView.as_view(),
        name="classroom_update",
    ),
    path(
        "subjectroom/classroom/<int:pk>/delete/",
        ClassroomDeleteView.as_view(),
        name="classroom_delete",
    ),
    path(
        "subjectroom/subject/create/",
        SubjectCreateView.as_view(),
        name="subject_create",
    ),
    path(
        "subjectroom/subject/<int:pk>/update/",
        SubjectUpdateView.as_view(),
        name="subject_update",
    ),
    path(
        "subjectroom/subject/<int:pk>/delete/",
        SubjectDeleteView.as_view(),
        name="subject_delete",
    ),
]
