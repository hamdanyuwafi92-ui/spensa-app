from django.urls import path
from core.views.activeclub import (
    ActiveClubListView,
    ActiveClubCreateView,
    ActiveClubUpdateView,
    ActiveClubDeleteView,
    ActiveClubManageView,
    ClubStudentDeleteView,
)

app_name = "core"

urlpatterns = [
    path("activeclub/", ActiveClubListView.as_view(), name="activeclub_list"),
    path(
        "activeclub/create/", ActiveClubCreateView.as_view(), name="activeclub_create"
    ),
    path(
        "activeclub/<int:pk>/update/",
        ActiveClubUpdateView.as_view(),
        name="activeclub_update",
    ),
    path(
        "activeclub/<int:pk>/delete/",
        ActiveClubDeleteView.as_view(),
        name="activeclub_delete",
    ),
    path(
        "activeclub/<int:pk>/manage/",
        ActiveClubManageView.as_view(),
        name="activeclub_manage",
    ),
    path(
        "activeclub/<int:club_pk>/student/<int:student_pk>/delete/",
        ClubStudentDeleteView.as_view(),
        name="activeclub_student_delete",
    ),
]
