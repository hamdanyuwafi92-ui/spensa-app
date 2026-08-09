from django.urls import path
from core.views.club import (
    ClubManageView,
    ClubCreateView,
    ClubUpdateView,
    ClubDeleteView,
)

app_name = "core"

urlpatterns = [
    path("club/", ClubManageView.as_view(), name="club_manage"),
    path("club/create/", ClubCreateView.as_view(), name="club_create"),
    path("club/<int:pk>/update/", ClubUpdateView.as_view(), name="club_update"),
    path("club/<int:pk>/delete/", ClubDeleteView.as_view(), name="club_delete"),
]
