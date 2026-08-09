from django.urls import path

from core.views.album import (
    AlbumCreateView,
    AlbumDeleteView,
    AlbumListView,
    AlbumManageView,
    AlbumUpdateView,
    PhotoDeleteView,
)

app_name = "core"

urlpatterns = [
    path("album/", AlbumListView.as_view(), name="album_list"),
    path("album/create/", AlbumCreateView.as_view(), name="album_create"),
    path("album/<slug:slug>/update/", AlbumUpdateView.as_view(), name="album_update"),
    path("album/<slug:slug>/delete/", AlbumDeleteView.as_view(), name="album_delete"),
    path("album/<slug:slug>/manage/", AlbumManageView.as_view(), name="album_manage"),
    path("photo/<int:pk>/delete/", PhotoDeleteView.as_view(), name="photo_delete"),
]
