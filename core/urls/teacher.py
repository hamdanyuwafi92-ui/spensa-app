from django.urls import path
from core.views.teacher import (
    TeacherListView,
    TeacherCreateView,
    TeacherUpdateView,
    TeacherDeleteView,
    TeacherDetailView,
    TeacherResetPasswordView,
)

app_name = "core"

urlpatterns = [
    path("teacher/", TeacherListView.as_view(), name="teacher_list"),
    path("teacher/create/", TeacherCreateView.as_view(), name="teacher_create"),
    path(
        "teacher/<int:pk>/update/", TeacherUpdateView.as_view(), name="teacher_update"
    ),
    path(
        "teacher/<int:pk>/delete/", TeacherDeleteView.as_view(), name="teacher_delete"
    ),
    path(
        "teacher/<int:pk>/detail/", TeacherDetailView.as_view(), name="teacher_detail"
    ),
    path(
        "teacher/<int:pk>/reset-password/",
        TeacherResetPasswordView.as_view(),
        name="teacher_reset_password",
    ),
]
