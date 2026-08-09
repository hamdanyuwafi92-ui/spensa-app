from django.urls import path

from core.views.year import (
    ActiveYearCreateView,
    ActiveYearDeleteView,
    ActiveYearUpdateView,
    SemesterCreateView,
    SemesterDeleteView,
    SemesterUpdateView,
    YearCreateView,
    YearDeleteView,
    YearManageView,
    YearUpdateView,
)

app_name = "core"

urlpatterns = [
    path("year/", YearManageView.as_view(), name="year_manage"),
    path("year/year/create/", YearCreateView.as_view(), name="year_create"),
    path("year/year/<int:pk>/update/", YearUpdateView.as_view(), name="year_update"),
    path("year/year/<int:pk>/delete/", YearDeleteView.as_view(), name="year_delete"),
    path("year/semester/create/", SemesterCreateView.as_view(), name="semester_create"),
    path(
        "year/semester/<int:pk>/update/",
        SemesterUpdateView.as_view(),
        name="semester_update",
    ),
    path(
        "year/semester/<int:pk>/delete/",
        SemesterDeleteView.as_view(),
        name="semester_delete",
    ),
    path(
        "year/active/create/", ActiveYearCreateView.as_view(), name="active_year_create"
    ),
    path(
        "year/active/<int:pk>/update/",
        ActiveYearUpdateView.as_view(),
        name="active_year_update",
    ),
    path(
        "year/active/<int:pk>/delete/",
        ActiveYearDeleteView.as_view(),
        name="active_year_delete",
    ),
]
