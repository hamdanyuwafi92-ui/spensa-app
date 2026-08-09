from typing import ClassVar
from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from django_summernote.widgets import SummernoteWidget

from core.models import Article, Tag

from .base import GlobalContextMixin


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ("title", "thumbnail", "category", "tags", "content", "status")
        # widgets: ClassVar[dict] = {"tags": forms.CheckboxSelectMultiple}
        widgets = {
            "content": SummernoteWidget(),
            "tags": forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(
                field.widget,
                (
                    forms.TextInput,
                    forms.Textarea,
                    forms.Select,
                    forms.EmailInput,
                    forms.URLInput,
                    forms.NumberInput,
                    forms.PasswordInput,
                    forms.ClearableFileInput,
                ),
            ):
                field.widget.attrs.setdefault("class", "form-control")
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.setdefault("class", "checkbox-group")


class ArticleContextMixin(LoginRequiredMixin, GlobalContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_articles"] = Article.objects.count()
        context["published_articles"] = Article.objects.filter(status="publish").count()
        context["draft_articles"] = Article.objects.filter(status="draft").count()
        context["breadcrumb_text"] = "Artikel"
        return context


class ArticleListView(ArticleContextMixin, ListView):
    template_name = "core/article.html"
    context_object_name = "articles"
    paginate_by = 10

    def get_queryset(self):
        return Article.objects.select_related("created_by").order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_mode"] = "list"
        return context


class ArticleCreateView(ArticleContextMixin, SuccessMessageMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = "core/article.html"
    success_url = reverse_lazy("core:article_list")
    success_message = "Artikel berhasil dibuat."

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_mode"] = "create"
        context["form_title"] = "Tambah Artikel Baru"
        context["all_tags"] = Tag.objects.all()
        return context


class ArticleUpdateView(ArticleContextMixin, SuccessMessageMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = "core/article.html"
    success_url = reverse_lazy("core:article_list")
    success_message = "Artikel berhasil diperbarui."

    def get_queryset(self):
        return Article.objects.filter(created_by=self.request.user)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.created_by != self.request.user:
            raise Http404("Artikel tidak ditemukan.")
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_mode"] = "update"
        context["form_title"] = "Edit Artikel"
        context["all_tags"] = Tag.objects.all()
        return context


class ArticleDeleteView(ArticleContextMixin, SuccessMessageMixin, DeleteView):
    model = Article
    template_name = "core/article.html"
    success_url = reverse_lazy("core:article_list")
    success_message = "Artikel berhasil dihapus."

    def get_queryset(self):
        return Article.objects.filter(created_by=self.request.user)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.created_by != self.request.user:
            raise Http404("Artikel tidak ditemukan.")
        return obj

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)
