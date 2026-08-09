from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView

from blog.forms import CommentForm
from core.models import Article, Category


class ArticleListView(ListView):
    model = Article
    template_name = "blog/artikel_list.html"
    context_object_name = "articles"
    paginate_by = 6

    def get_queryset(self):
        return (
            Article.objects.filter(status="publish")
            .select_related("category")
            .prefetch_related("tags")
            .order_by("-created_at")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = "blog/artikel_detail.html"
    context_object_name = "article"

    def get_queryset(self):
        return (
            Article.objects.filter(status="publish")
            .select_related("category", "created_by")
            .prefetch_related("tags", "comments")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["comment_form"] = CommentForm()
        context["comments"] = self.object.comments.filter(active=True).order_by(
            "-created_at"
        )
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = self.object
            comment.save()
            messages.success(request, "Komentar berhasil dikirim.")
        else:
            messages.error(
                request, "Gagal mengirim komentar. Periksa kembali data Anda."
            )
        return redirect("blog:single", slug=self.object.slug)
