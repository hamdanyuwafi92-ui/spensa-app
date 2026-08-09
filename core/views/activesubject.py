from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView
from django.views.generic.edit import CreateView

from core.forms.activesubject import ActiveSubjectForm
from core.models import ActiveSubject, ActiveYear, Classroom, Subject, Teacher
from .base import BaseAccessMixin, ModalFormMixin


class ActiveSubjectContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb_text"] = "Mapel Aktif"
        return context


class ActiveSubjectBaseMixin(BaseAccessMixin, ActiveSubjectContextMixin):
    pass


class ActiveSubjectListView(ActiveSubjectBaseMixin, ListView):
    template_name = "core/activesubject.html"
    context_object_name = "activesubjects"
    paginate_by = 10

    def get_queryset(self):
        return ActiveSubject.objects.select_related(
            "activeyear", "subject", "classroom", "teacher"
        ).order_by("-id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_year = ActiveYear.get_active()
        context["active_year"] = active_year
        context["subjects"] = Subject.objects.all()
        context["classrooms"] = Classroom.objects.all()
        context["teachers"] = Teacher.objects.filter(
            job__in=["Guru", "Developer", "Administrator"]
        )
        if not active_year:
            messages.warning(
                self.request,
                "Tidak ada tahun ajaran aktif. Silakan aktifkan satu tahun ajaran terlebih dahulu.",
            )
        return context


class ActiveSubjectCreateView(
    ActiveSubjectBaseMixin, ModalFormMixin, SuccessMessageMixin, CreateView
):
    model = ActiveSubject
    form_class = ActiveSubjectForm
    form_type = "activesubject"
    template_name = "core/activesubject.html"
    success_url = reverse_lazy("core:activesubject_list")
    success_message = "Mapel aktif berhasil ditambahkan."

    def dispatch(self, request, *args, **kwargs):
        if not ActiveYear.get_active():
            messages.warning(
                request,
                "Tidak ada tahun ajaran aktif. Silakan aktifkan satu tahun ajaran terlebih dahulu.",
            )
            return redirect("core:year_manage")
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        active_year = ActiveYear.get_active()
        if active_year:
            initial["activeyear"] = active_year
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_year"] = ActiveYear.get_active()
        context["subjects"] = Subject.objects.all()
        context["classrooms"] = Classroom.objects.all()
        context["teachers"] = Teacher.objects.filter(
            job__in=["Guru", "Developer", "Administrator"]
        )
        return context

    def form_invalid(self, form):
        messages.error(self.request, "Gagal menyimpan. Periksa kembali data Anda.")
        return redirect(self.success_url)


class ActiveSubjectUpdateView(
    ActiveSubjectBaseMixin, ModalFormMixin, SuccessMessageMixin, UpdateView
):
    model = ActiveSubject
    form_class = ActiveSubjectForm
    form_type = "activesubject"
    template_name = "core/activesubject.html"
    success_url = reverse_lazy("core:activesubject_list")
    success_message = "Mapel aktif berhasil diperbarui."

    def dispatch(self, request, *args, **kwargs):
        if not ActiveYear.get_active():
            messages.warning(
                request,
                "Tidak ada tahun ajaran aktif. Silakan aktifkan satu tahun ajaran terlebih dahulu.",
            )
            return redirect("core:year_manage")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_year"] = ActiveYear.get_active()
        context["subjects"] = Subject.objects.all()
        context["classrooms"] = Classroom.objects.all()
        context["teachers"] = Teacher.objects.filter(
            job__in=["Guru", "Developer", "Administrator"]
        )
        return context

    def form_invalid(self, form):
        messages.error(self.request, "Gagal menyimpan. Periksa kembali data Anda.")
        return redirect(self.success_url)


class ActiveSubjectDeleteView(ActiveSubjectBaseMixin, SuccessMessageMixin, DeleteView):
    model = ActiveSubject
    template_name = "core/activesubject.html"
    success_url = reverse_lazy("core:activesubject_list")
    success_message = "Mapel aktif berhasil dihapus."

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)
