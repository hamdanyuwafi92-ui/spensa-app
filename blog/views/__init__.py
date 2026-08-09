from .album import AlbumDetailView, AlbumListView
from .article import ArticleDetailView, ArticleListView
from .index import IndexView
from .kategori import CategoryArticleListView
from .page import PageDetailView, PageListView
from .search import SearchView
from .school import SchoolDetailView
from .staff import TeacherListView, StudentListView
from .contact import ContactView

__all__ = [
    "AlbumDetailView",
    "AlbumListView",
    "ArticleDetailView",
    "ArticleListView",
    "CategoryArticleListView",
    "IndexView",
    "PageDetailView",
    "PageListView",
    "SearchView",
    "SchoolDetailView",
    "TeacherListView",
    "StudentListView",
    "ContactView",
]
