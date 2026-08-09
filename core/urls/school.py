from django.urls import path
from core.views.school import SchoolDetailView, SchoolUpdateView

app_name = "core"

urlpatterns = [
    path("school/", SchoolDetailView.as_view(), name="school_detail"),
    path("school/edit/", SchoolUpdateView.as_view(), name="school_edit"),
]
