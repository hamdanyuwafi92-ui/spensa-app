from django.urls import path

from core.views.blog import (
    ArticleCreateView,
    ArticleDeleteView,
    ArticleListView,
    ArticleUpdateView,
)

app_name = "core"

urlpatterns = [
    path("article/", ArticleListView.as_view(), name="article_list"),
    path("article/create/", ArticleCreateView.as_view(), name="article_create"),
    path(
        "article/<slug:slug>/update/",
        ArticleUpdateView.as_view(),
        name="article_update",
    ),
    path(
        "article/<slug:slug>/delete/",
        ArticleDeleteView.as_view(),
        name="article_delete",
    ),
]
