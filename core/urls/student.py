from django.urls import path
from core.views.student import (
    StudentListView,
    StudentCreateView,
    StudentUpdateView,
    StudentDeleteView,
    StudentDetailView,
    StudentResetPasswordView,
)

app_name = "core"

urlpatterns = [
    path("student/", StudentListView.as_view(), name="student_list"),
    path("student/create/", StudentCreateView.as_view(), name="student_create"),
    path(
        "student/<int:pk>/update/", StudentUpdateView.as_view(), name="student_update"
    ),
    path(
        "student/<int:pk>/delete/", StudentDeleteView.as_view(), name="student_delete"
    ),
    path(
        "student/<int:pk>/detail/", StudentDetailView.as_view(), name="student_detail"
    ),
    path(
        "student/<int:pk>/reset-password/",
        StudentResetPasswordView.as_view(),
        name="student_reset_password",
    ),
]
