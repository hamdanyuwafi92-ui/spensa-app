from django.db.models import Q
from django.views.generic import ListView
from core.models import Article


class SearchView(ListView):
    model = Article
    template_name = "blog/search.html"
    context_object_name = "articles"
    paginate_by = 6

    def get_queryset(self):
        query = self.request.GET.get("q", "").strip()
        if query:
            return (
                Article.objects.filter(
                    Q(status="publish")
                    & (Q(title__icontains=query) | Q(content__icontains=query))
                )
                .select_related("category")
                .order_by("-created_at")
            )
        return Article.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "")
        return context
