from django.views.generic import ListView, DetailView
from core.models import Page


class PageListView(ListView):
    model = Page
    template_name = "blog/page_list.html"
    context_object_name = "pages"
    paginate_by = 6

    def get_queryset(self):
        return Page.objects.all().order_by("-created_at")


class PageDetailView(DetailView):
    model = Page
    template_name = "blog/page_detail.html"
    context_object_name = "page"
