from django.views.generic import TemplateView
from core.models import Article
from blog.models import Feature
from blog.models import HeroSlide, Feature


class IndexView(TemplateView):
    template_name = "blog/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["articles"] = (
            Article.objects.filter(status="publish")
            .select_related("category")
            .prefetch_related("tags")
            .order_by("-created_at")[:6]
        )
        context["features"] = Feature.objects.all()
        context["hero_slides"] = HeroSlide.objects.all()
        return context
