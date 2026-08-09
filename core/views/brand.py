from django.contrib import messages
from django.views.generic import TemplateView, UpdateView
from django.urls import reverse_lazy

from core.models import Brand
from core.forms.brand import BrandForm
from core.utilities.access import JobAccessMixin
from .base import GlobalContextMixin


class DeveloperAccessMixin(JobAccessMixin):
    allowed_jobs = ["Developer"]


class BrandBaseMixin(DeveloperAccessMixin, GlobalContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb_text"] = "Brand"
        return context


class BrandDetailView(BrandBaseMixin, TemplateView):
    template_name = "core/brand/brand.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        brand = Brand.get_solo()
        context["brand"] = brand
        context["has_data"] = bool(brand.pk and brand.name)
        return context


class BrandUpdateView(BrandBaseMixin, UpdateView):
    form_class = BrandForm
    template_name = "core/brand/brand_form.html"
    success_url = reverse_lazy("core:brand_detail")

    def get_object(self, queryset=None):
        return Brand.get_solo()

    def form_valid(self, form):
        messages.success(self.request, "Data brand berhasil disimpan.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Gagal menyimpan. Periksa kembali data Anda.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Edit Brand"
        context["breadcrumb_text"] = "Edit Brand"
        return context
