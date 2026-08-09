from django.views.generic import ListView, DetailView
from core.models import Album


class AlbumListView(ListView):
    model = Album
    template_name = "blog/album_list.html"
    context_object_name = "albums"
    paginate_by = 6

    def get_queryset(self):
        return Album.objects.all().order_by("-created_at")


class AlbumDetailView(DetailView):
    model = Album
    template_name = "blog/album_detail.html"
    context_object_name = "album"

    def get_queryset(self):
        return Album.objects.prefetch_related("photo_set")
