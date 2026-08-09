from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView, DeleteView
from django.views.generic.edit import CreateView

from core.forms.year import ActiveYearForm, SemesterForm, YearForm
from core.models import ActiveYear, Semester, Year
from .base import BaseAccessMixin, ModalFormMixin


class YearContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["years"] = Year.objects.all()
        context["semesters"] = Semester.objects.all()
        active_list = ActiveYear.objects.select_related("year", "semester").order_by(
            "id"
        )
        paginator = Paginator(active_list, 10)
        page = self.request.GET.get("page")
        context["active_years"] = paginator.get_page(page)
        context["breadcrumb_text"] = "Tahun Ajaran"
        return context


class YearBaseMixin(BaseAccessMixin, YearContextMixin):
    pass


class YearManageView(YearBaseMixin, TemplateView):
    template_name = "core/year.html"


class YearCreateView(YearBaseMixin, ModalFormMixin, SuccessMessageMixin, CreateView):
    model = Year
    form_class = YearForm
    form_type = "year"
    success_url = reverse_lazy("core:year_manage")
    success_message = "Tahun ajaran berhasil ditambahkan."


class YearUpdateView(YearBaseMixin, ModalFormMixin, SuccessMessageMixin, UpdateView):
    model = Year
    form_class = YearForm
    form_type = "year"
    success_url = reverse_lazy("core:year_manage")
    success_message = "Tahun ajaran berhasil diperbarui."


class YearDeleteView(YearBaseMixin, SuccessMessageMixin, DeleteView):
    model = Year
    success_url = reverse_lazy("core:year_manage")
    success_message = "Tahun ajaran berhasil dihapus."

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class SemesterCreateView(
    YearBaseMixin, ModalFormMixin, SuccessMessageMixin, CreateView
):
    model = Semester
    form_class = SemesterForm
    form_type = "semester"
    success_url = reverse_lazy("core:year_manage")
    success_message = "Semester berhasil ditambahkan."


class SemesterUpdateView(
    YearBaseMixin, ModalFormMixin, SuccessMessageMixin, UpdateView
):
    model = Semester
    form_class = SemesterForm
    form_type = "semester"
    success_url = reverse_lazy("core:year_manage")
    success_message = "Semester berhasil diperbarui."


class SemesterDeleteView(YearBaseMixin, SuccessMessageMixin, DeleteView):
    model = Semester
    success_url = reverse_lazy("core:year_manage")
    success_message = "Semester berhasil dihapus."

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class ActiveYearCreateView(
    YearBaseMixin, ModalFormMixin, SuccessMessageMixin, CreateView
):
    model = ActiveYear
    form_class = ActiveYearForm
    form_type = "active_year"
    success_url = reverse_lazy("core:year_manage")
    success_message = "Tahun aktif berhasil ditambahkan."


class ActiveYearUpdateView(
    YearBaseMixin, ModalFormMixin, SuccessMessageMixin, UpdateView
):
    model = ActiveYear
    form_class = ActiveYearForm
    form_type = "active_year"
    success_url = reverse_lazy("core:year_manage")
    success_message = "Tahun aktif berhasil diperbarui."


class ActiveYearDeleteView(YearBaseMixin, SuccessMessageMixin, DeleteView):
    model = ActiveYear
    success_url = reverse_lazy("core:year_manage")
    success_message = "Tahun aktif berhasil dihapus."

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


# from django.contrib import messages
# from django.contrib.messages.views import SuccessMessageMixin
# from django.core.paginator import Paginator
# from django.urls import reverse_lazy
# from django.views.generic import TemplateView, UpdateView, DeleteView
# from django.views.generic.edit import CreateView

# from core.forms.year import ActiveYearForm, SemesterForm, YearForm
# from core.models import ActiveYear, Semester, Year
# from .base import BaseAccessMixin, ModalFormMixin


# class YearContextMixin:
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["years"] = Year.objects.all()
#         context["semesters"] = Semester.objects.all()
#         active_list = ActiveYear.objects.select_related("year", "semester").all()
#         paginator = Paginator(active_list, 10)
#         page = self.request.GET.get("page")
#         context["active_years"] = paginator.get_page(page)
#         context["breadcrumb_text"] = "Tahun Ajaran"
#         return context


# class YearBaseMixin(BaseAccessMixin, YearContextMixin):
#     pass


# class YearManageView(YearBaseMixin, TemplateView):
#     template_name = "core/year.html"


# class YearCreateView(YearBaseMixin, ModalFormMixin, SuccessMessageMixin, CreateView):
#     model = Year
#     form_class = YearForm
#     form_type = "year"
#     success_url = reverse_lazy("core:year_manage")
#     success_message = "Tahun ajaran berhasil ditambahkan."


# class YearUpdateView(YearBaseMixin, ModalFormMixin, SuccessMessageMixin, UpdateView):
#     model = Year
#     form_class = YearForm
#     form_type = "year"
#     success_url = reverse_lazy("core:year_manage")
#     success_message = "Tahun ajaran berhasil diperbarui."


# class YearDeleteView(YearBaseMixin, SuccessMessageMixin, DeleteView):
#     model = Year
#     success_url = reverse_lazy("core:year_manage")
#     success_message = "Tahun ajaran berhasil dihapus."

#     def delete(self, request, *args, **kwargs):
#         messages.success(self.request, self.success_message)
#         return super().delete(request, *args, **kwargs)


# class SemesterCreateView(
#     YearBaseMixin, ModalFormMixin, SuccessMessageMixin, CreateView
# ):
#     model = Semester
#     form_class = SemesterForm
#     form_type = "semester"
#     success_url = reverse_lazy("core:year_manage")
#     success_message = "Semester berhasil ditambahkan."


# class SemesterUpdateView(
#     YearBaseMixin, ModalFormMixin, SuccessMessageMixin, UpdateView
# ):
#     model = Semester
#     form_class = SemesterForm
#     form_type = "semester"
#     success_url = reverse_lazy("core:year_manage")
#     success_message = "Semester berhasil diperbarui."


# class SemesterDeleteView(YearBaseMixin, SuccessMessageMixin, DeleteView):
#     model = Semester
#     success_url = reverse_lazy("core:year_manage")
#     success_message = "Semester berhasil dihapus."

#     def delete(self, request, *args, **kwargs):
#         messages.success(self.request, self.success_message)
#         return super().delete(request, *args, **kwargs)


# class ActiveYearCreateView(
#     YearBaseMixin, ModalFormMixin, SuccessMessageMixin, CreateView
# ):
#     model = ActiveYear
#     form_class = ActiveYearForm
#     form_type = "active_year"
#     success_url = reverse_lazy("core:year_manage")
#     success_message = "Tahun aktif berhasil ditambahkan."


# class ActiveYearUpdateView(
#     YearBaseMixin, ModalFormMixin, SuccessMessageMixin, UpdateView
# ):
#     model = ActiveYear
#     form_class = ActiveYearForm
#     form_type = "active_year"
#     success_url = reverse_lazy("core:year_manage")
#     success_message = "Tahun aktif berhasil diperbarui."


# class ActiveYearDeleteView(YearBaseMixin, SuccessMessageMixin, DeleteView):
#     model = ActiveYear
#     success_url = reverse_lazy("core:year_manage")
#     success_message = "Tahun aktif berhasil dihapus."

#     def delete(self, request, *args, **kwargs):
#         messages.success(self.request, self.success_message)
#         return super().delete(request, *args, **kwargs)


# from django.contrib import messages
# from django.contrib.messages.views import SuccessMessageMixin
# from django.core.paginator import Paginator
# from django.urls import reverse_lazy
# from django.views.generic import TemplateView, UpdateView, DeleteView
# from django.views.generic.edit import CreateView

# from core.forms.year import ActiveYearForm, SemesterForm, YearForm
# from core.models import ActiveYear, Semester, Year
# from .base import BaseAccessMixin


# class YearContextMixin:
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["years"] = Year.objects.all()
#         context["semesters"] = Semester.objects.all()
#         active_list = ActiveYear.objects.select_related("year", "semester").all()
#         paginator = Paginator(active_list, 10)
#         page = self.request.GET.get("page")
#         context["active_years"] = paginator.get_page(page)
#         context["breadcrumb_text"] = "Tahun Ajaran"
#         return context


# class YearBaseMixin(BaseAccessMixin, YearContextMixin):
#     pass


# class YearManageView(YearBaseMixin, TemplateView):
#     template_name = "core/year.html"


# class YearCreateView(YearBaseMixin, SuccessMessageMixin, CreateView):
#     model = Year
#     form_class = YearForm
#     success_url = reverse_lazy("core:year_manage")
#     success_message = "Tahun ajaran berhasil ditambahkan."


# class YearUpdateView(YearBaseMixin, SuccessMessageMixin, UpdateView):
#     model = Year
#     form_class = YearForm
#     success_url = reverse_lazy("core:year_manage")
#     success_message = "Tahun ajaran berhasil diperbarui."


# class YearDeleteView(YearBaseMixin, SuccessMessageMixin, DeleteView):
#     model = Year
#     success_url = reverse_lazy("core:year_manage")
#     success_message = "Tahun ajaran berhasil dihapus."

#     def delete(self, request, *args, **kwargs):
#         messages.success(self.request, self.success_message)
#         return super().delete(request, *args, **kwargs)


# class SemesterCreateView(YearBaseMixin, SuccessMessageMixin, CreateView):
#     model = Semester
#     form_class = SemesterForm
#     success_url = reverse_lazy("core:year_manage")
#     success_message = "Semester berhasil ditambahkan."


# class SemesterUpdateView(YearBaseMixin, SuccessMessageMixin, UpdateView):
#     model = Semester
#     form_class = SemesterForm
#     success_url = reverse_lazy("core:year_manage")
#     success_message = "Semester berhasil diperbarui."


# class SemesterDeleteView(YearBaseMixin, SuccessMessageMixin, DeleteView):
#     model = Semester
#     success_url = reverse_lazy("core:year_manage")
#     success_message = "Semester berhasil dihapus."

#     def delete(self, request, *args, **kwargs):
#         messages.success(self.request, self.success_message)
#         return super().delete(request, *args, **kwargs)


# class ActiveYearCreateView(YearBaseMixin, SuccessMessageMixin, CreateView):
#     model = ActiveYear
#     form_class = ActiveYearForm
#     success_url = reverse_lazy("core:year_manage")
#     success_message = "Tahun aktif berhasil ditambahkan."


# class ActiveYearUpdateView(YearBaseMixin, SuccessMessageMixin, UpdateView):
#     model = ActiveYear
#     form_class = ActiveYearForm
#     success_url = reverse_lazy("core:year_manage")
#     success_message = "Tahun aktif berhasil diperbarui."


# class ActiveYearDeleteView(YearBaseMixin, SuccessMessageMixin, DeleteView):
#     model = ActiveYear
#     success_url = reverse_lazy("core:year_manage")
#     success_message = "Tahun aktif berhasil dihapus."

#     def delete(self, request, *args, **kwargs):
#         messages.success(self.request, self.success_message)
#         return super().delete(request, *args, **kwargs)


# from typing import ClassVar

# from django.contrib import messages
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.messages.views import SuccessMessageMixin
# from django.core.paginator import Paginator
# from django.urls import reverse_lazy
# from django.views.generic import DeleteView, TemplateView, UpdateView
# from django.views.generic.edit import CreateView

# from core.forms.year import ActiveYearForm, SemesterForm, YearForm
# from core.models import ActiveYear, Semester, Year
# from core.utilities.access import JobAccessMixin

# from .base import GlobalContextMixin


# class YearAccessMixin(JobAccessMixin):
#     allowed_jobs: ClassVar[list[str]] = ["Developer", "Administrator"]


# class YearManageView(
#     YearAccessMixin, LoginRequiredMixin, GlobalContextMixin, TemplateView
# ):
#     template_name = "core/year.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["years"] = Year.objects.all()
#         context["semesters"] = Semester.objects.all()
#         active_list = ActiveYear.objects.select_related("year", "semester").all()
#         paginator = Paginator(active_list, 10)
#         page = self.request.GET.get("page")
#         context["active_years"] = paginator.get_page(page)
#         context["breadcrumb_text"] = "Tahun Ajaran"
#         return context


# class YearCreateView(YearAccessMixin, SuccessMessageMixin, CreateView):
#     model = Year
#     form_class = YearForm
#     success_url = reverse_lazy("core:year_manage")
#     success_message = "Tahun ajaran berhasil ditambahkan."


# class YearUpdateView(YearAccessMixin, SuccessMessageMixin, UpdateView):
#     model = Year
#     form_class = YearForm
#     success_url = reverse_lazy("core:year_manage")
#     success_message = "Tahun ajaran berhasil diperbarui."


# class YearDeleteView(YearAccessMixin, SuccessMessageMixin, DeleteView):
#     model = Year
#     success_url = reverse_lazy("core:year_manage")
#     success_message = "Tahun ajaran berhasil dihapus."

#     def delete(self, request, *args, **kwargs):
#         messages.success(self.request, self.success_message)
#         return super().delete(request, *args, **kwargs)


# class SemesterCreateView(YearAccessMixin, SuccessMessageMixin, CreateView):
#     model = Semester
#     form_class = SemesterForm
#     success_url = reverse_lazy("core:year_manage")
#     success_message = "Semester berhasil ditambahkan."


# class SemesterUpdateView(YearAccessMixin, SuccessMessageMixin, UpdateView):
#     model = Semester
#     form_class = SemesterForm
#     success_url = reverse_lazy("core:year_manage")
#     success_message = "Semester berhasil diperbarui."


# class SemesterDeleteView(YearAccessMixin, SuccessMessageMixin, DeleteView):
#     model = Semester
#     success_url = reverse_lazy("core:year_manage")
#     success_message = "Semester berhasil dihapus."

#     def delete(self, request, *args, **kwargs):
#         messages.success(self.request, self.success_message)
#         return super().delete(request, *args, **kwargs)


# class ActiveYearCreateView(YearAccessMixin, SuccessMessageMixin, CreateView):
#     model = ActiveYear
#     form_class = ActiveYearForm
#     success_url = reverse_lazy("core:year_manage")
#     success_message = "Tahun aktif berhasil ditambahkan."


# class ActiveYearUpdateView(YearAccessMixin, SuccessMessageMixin, UpdateView):
#     model = ActiveYear
#     form_class = ActiveYearForm
#     success_url = reverse_lazy("core:year_manage")
#     success_message = "Tahun aktif berhasil diperbarui."


# class ActiveYearDeleteView(YearAccessMixin, SuccessMessageMixin, DeleteView):
#     model = ActiveYear
#     success_url = reverse_lazy("core:year_manage")
#     success_message = "Tahun aktif berhasil dihapus."

#     def delete(self, request, *args, **kwargs):
#         messages.success(self.request, self.success_message)
#         return super().delete(request, *args, **kwargs)
