from django.urls import path
from blog.views import (
    IndexView,
    ArticleListView,
    ArticleDetailView,
    PageListView,
    PageDetailView,
    AlbumListView,
    AlbumDetailView,
    CategoryArticleListView,
    SearchView,
)
from blog.views.school import SchoolDetailView
from blog.views.staff import TeacherListView, StudentListView
from blog.views.contact import ContactView

app_name = "blog"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("sekolah/", SchoolDetailView.as_view(), name="school_detail"),
    path("guru/", TeacherListView.as_view(), name="teacher_list"),
    path("siswa/", StudentListView.as_view(), name="student_list"),
    path("artikel/", ArticleListView.as_view(), name="artikel"),
    path("artikel/<slug:slug>/", ArticleDetailView.as_view(), name="single"),
    path("page/", PageListView.as_view(), name="page"),
    path("page/<slug:slug>/", PageDetailView.as_view(), name="page_detail"),
    path("galeri/", AlbumListView.as_view(), name="galeri"),
    path("galeri/<slug:slug>/", AlbumDetailView.as_view(), name="album"),
    path("kategori/", CategoryArticleListView.as_view(), name="kategori"),
    path("cari/", SearchView.as_view(), name="search"),
    path("kontak/", ContactView.as_view(), name="kontak"),
]
