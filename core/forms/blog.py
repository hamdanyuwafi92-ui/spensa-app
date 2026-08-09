from typing import ClassVar

from django import forms

from core.models import Article

from .base import FormControlMixin


class ArticleForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = Article
        fields = ("title", "thumbnail", "category", "tags", "content", "status")
        widgets: ClassVar[dict] = {"tags": forms.CheckboxSelectMultiple}
