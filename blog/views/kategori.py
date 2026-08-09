from django.views.generic import ListView
from core.models import Article, Category


class CategoryArticleListView(ListView):
    model = Article
    template_name = "blog/kategori.html"
    context_object_name = "articles"
    paginate_by = 6

    def get_queryset(self):
        queryset = (
            Article.objects.filter(status="publish")
            .select_related("category")
            .order_by("-created_at")
        )
        cat_id = self.request.GET.get("cat")
        if cat_id and cat_id.isdigit():
            queryset = queryset.filter(category_id=int(cat_id))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        cat_id = self.request.GET.get("cat")
        if cat_id and cat_id.isdigit():
            try:
                context["selected_category"] = Category.objects.get(pk=int(cat_id))
            except Category.DoesNotExist:
                pass
        return context
