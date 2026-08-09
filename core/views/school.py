from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, UpdateView
from django.urls import reverse_lazy

from core.models import School
from core.forms.school import SchoolForm
from .base import BaseAccessMixin, GlobalContextMixin


class SchoolBaseMixin(BaseAccessMixin, GlobalContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb_text"] = "Sekolah"
        return context


class SchoolDetailView(SchoolBaseMixin, TemplateView):
    template_name = "core/school/school.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school = School.get_solo()
        context["school"] = school
        context["has_data"] = bool(school.pk and school.name)
        return context


class SchoolUpdateView(SchoolBaseMixin, UpdateView):
    form_class = SchoolForm
    template_name = "core/school/school_form.html"
    success_url = reverse_lazy("core:school_detail")

    def get_object(self, queryset=None):
        return School.get_solo()

    def form_valid(self, form):
        messages.success(self.request, "Data sekolah berhasil disimpan.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Gagal menyimpan. Periksa kembali data Anda.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Edit Data Sekolah"
        context["breadcrumb_text"] = "Edit Sekolah"
        return context
