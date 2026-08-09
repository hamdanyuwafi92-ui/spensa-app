from typing import ClassVar

from django import forms
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from django_summernote.widgets import SummernoteWidget

from core.models import Page
from core.utilities.validators import validate_logo
from .base import BaseAccessMixin


class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ("title", "thumbnail", "content")
        # widgets: ClassVar[dict] = {}
        widgets = {
            "content": SummernoteWidget(),
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
        self.fields["thumbnail"].validators.append(validate_logo)


class PageContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_pages"] = Page.objects.count()
        context["breadcrumb_text"] = "Halaman"
        return context


class PageBaseMixin(BaseAccessMixin, PageContextMixin):
    pass


class PageListView(PageBaseMixin, ListView):
    template_name = "core/page.html"
    context_object_name = "pages"
    paginate_by = 10

    def get_queryset(self):
        return Page.objects.select_related("created_by").order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_mode"] = "list"
        return context


class PageCreateView(PageBaseMixin, SuccessMessageMixin, CreateView):
    model = Page
    form_class = PageForm
    template_name = "core/page.html"
    success_url = reverse_lazy("core:page_list")
    success_message = "Halaman berhasil dibuat."

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_mode"] = "create"
        context["form_title"] = "Tambah Halaman Baru"
        return context


class PageUpdateView(PageBaseMixin, SuccessMessageMixin, UpdateView):
    model = Page
    form_class = PageForm
    template_name = "core/page.html"
    success_url = reverse_lazy("core:page_list")
    success_message = "Halaman berhasil diperbarui."

    def get_queryset(self):
        return Page.objects.filter(created_by=self.request.user)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.created_by != self.request.user:
            raise Http404("Halaman tidak ditemukan.")
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_mode"] = "update"
        context["form_title"] = "Edit Halaman"
        return context


class PageDeleteView(PageBaseMixin, SuccessMessageMixin, DeleteView):
    model = Page
    template_name = "core/page.html"
    success_url = reverse_lazy("core:page_list")
    success_message = "Halaman berhasil dihapus."

    def get_queryset(self):
        return Page.objects.filter(created_by=self.request.user)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.created_by != self.request.user:
            raise Http404("Halaman tidak ditemukan.")
        return obj

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


# from typing import ClassVar

# from django import forms
# from django.contrib import messages
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.messages.views import SuccessMessageMixin
# from django.http import Http404
# from django.urls import reverse_lazy
# from django.views.generic import CreateView, DeleteView, ListView, UpdateView

# from core.models import Page
# from core.utilities.access import JobAccessMixin
# from core.utilities.validators import validate_logo

# from .base import GlobalContextMixin


# class PageForm(forms.ModelForm):
#     class Meta:
#         model = Page
#         fields = ("title", "thumbnail", "content")
#         widgets: ClassVar[dict] = {}

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field in self.fields.values():
#             if isinstance(
#                 field.widget,
#                 (
#                     forms.TextInput,
#                     forms.Textarea,
#                     forms.Select,
#                     forms.EmailInput,
#                     forms.URLInput,
#                     forms.NumberInput,
#                     forms.PasswordInput,
#                     forms.ClearableFileInput,
#                 ),
#             ):
#                 field.widget.attrs.setdefault("class", "form-control")
#         self.fields["thumbnail"].validators.append(validate_logo)


# class PageAccessMixin(JobAccessMixin):
#     allowed_jobs: ClassVar[list[str]] = ["Developer", "Administrator"]


# class PageContextMixin(LoginRequiredMixin, GlobalContextMixin):
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["total_pages"] = Page.objects.count()
#         context["breadcrumb_text"] = "Halaman"
#         return context


# class PageListView(PageAccessMixin, PageContextMixin, ListView):
#     template_name = "core/page.html"
#     context_object_name = "pages"
#     paginate_by = 10

#     def get_queryset(self):
#         return Page.objects.select_related("created_by").order_by("-created_at")

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["view_mode"] = "list"
#         return context


# class PageCreateView(
#     PageAccessMixin, PageContextMixin, SuccessMessageMixin, CreateView
# ):
#     model = Page
#     form_class = PageForm
#     template_name = "core/page.html"
#     success_url = reverse_lazy("core:page_list")
#     success_message = "Halaman berhasil dibuat."

#     def form_valid(self, form):
#         form.instance.created_by = self.request.user
#         return super().form_valid(form)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["view_mode"] = "create"
#         context["form_title"] = "Tambah Halaman Baru"
#         return context


# class PageUpdateView(
#     PageAccessMixin, PageContextMixin, SuccessMessageMixin, UpdateView
# ):
#     model = Page
#     form_class = PageForm
#     template_name = "core/page.html"
#     success_url = reverse_lazy("core:page_list")
#     success_message = "Halaman berhasil diperbarui."

#     def get_queryset(self):
#         return Page.objects.filter(created_by=self.request.user)

#     def get_object(self, queryset=None):
#         obj = super().get_object(queryset)
#         if obj.created_by != self.request.user:
#             raise Http404("Halaman tidak ditemukan.")
#         return obj

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["view_mode"] = "update"
#         context["form_title"] = "Edit Halaman"
#         return context


# class PageDeleteView(
#     PageAccessMixin, PageContextMixin, SuccessMessageMixin, DeleteView
# ):
#     model = Page
#     template_name = "core/page.html"
#     success_url = reverse_lazy("core:page_list")
#     success_message = "Halaman berhasil dihapus."

#     def get_queryset(self):
#         return Page.objects.filter(created_by=self.request.user)

#     def get_object(self, queryset=None):
#         obj = super().get_object(queryset)
#         if obj.created_by != self.request.user:
#             raise Http404("Halaman tidak ditemukan.")
#         return obj

#     def delete(self, request, *args, **kwargs):
#         messages.success(self.request, self.success_message)
#         return super().delete(request, *args, **kwargs)
