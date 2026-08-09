from typing import ClassVar

from django import forms

from blog.models import Message
from core.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("name", "email", "body")
        widgets: ClassVar[dict] = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nama Anda",
                    "required": True,
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Email Anda (opsional)",
                }
            ),
            "body": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Tulis komentar...",
                    "rows": 3,
                    "required": True,
                }
            ),
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ("name", "email", "content")
        widgets: ClassVar[dict] = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Masukkan nama Anda",
                    "required": True,
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "nama@email.com",
                    "required": True,
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Tuliskan pesan atau pertanyaan Anda di sini...",
                    "rows": 5,
                    "required": True,
                }
            ),
        }
