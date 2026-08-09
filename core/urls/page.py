from django.urls import path

from core.views.page import (
    PageCreateView,
    PageDeleteView,
    PageListView,
    PageUpdateView,
)

app_name = "core"

urlpatterns = [
    path("page/", PageListView.as_view(), name="page_list"),
    path("page/create/", PageCreateView.as_view(), name="page_create"),
    path("page/<slug:slug>/update/", PageUpdateView.as_view(), name="page_update"),
    path("page/<slug:slug>/delete/", PageDeleteView.as_view(), name="page_delete"),
]
