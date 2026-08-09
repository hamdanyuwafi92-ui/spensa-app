from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, UpdateView, DeleteView
from django.views.generic.edit import CreateView

from core.forms.activeclub import ActiveClubForm, AddStudentToClubForm
from core.models import ActiveClub, ActiveYear, Club, Student, Teacher
from .base import BaseAccessMixin, ModalFormMixin


class ActiveClubContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb_text"] = "Klub Aktif"
        return context


class ActiveClubBaseMixin(BaseAccessMixin, ActiveClubContextMixin):
    pass


class ActiveClubListView(ActiveClubBaseMixin, ListView):
    template_name = "core/activeclub.html"
    context_object_name = "activeclubs"
    paginate_by = 10

    def get_queryset(self):
        return ActiveClub.objects.select_related(
            "activeyear", "club", "teacher"
        ).order_by("-id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_year = ActiveYear.get_active()
        context["active_year"] = active_year
        context["clubs"] = Club.objects.all()
        context["teachers"] = Teacher.objects.all()
        if not active_year:
            messages.warning(
                self.request,
                "Tidak ada tahun ajaran aktif. Silakan aktifkan satu tahun ajaran terlebih dahulu.",
            )
        return context


class ActiveClubCreateView(
    ActiveClubBaseMixin, ModalFormMixin, SuccessMessageMixin, CreateView
):
    model = ActiveClub
    form_class = ActiveClubForm
    form_type = "activeclub"
    template_name = "core/activeclub.html"
    success_url = reverse_lazy("core:activeclub_list")
    success_message = "Klub aktif berhasil ditambahkan."

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
        context["clubs"] = Club.objects.all()
        context["teachers"] = Teacher.objects.all()
        return context


class ActiveClubUpdateView(
    ActiveClubBaseMixin, ModalFormMixin, SuccessMessageMixin, UpdateView
):
    model = ActiveClub
    form_class = ActiveClubForm
    form_type = "activeclub"
    template_name = "core/activeclub.html"
    success_url = reverse_lazy("core:activeclub_list")
    success_message = "Klub aktif berhasil diperbarui."

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
        context["clubs"] = Club.objects.all()
        context["teachers"] = Teacher.objects.all()
        return context


class ActiveClubDeleteView(ActiveClubBaseMixin, SuccessMessageMixin, DeleteView):
    model = ActiveClub
    template_name = "core/activeclub.html"
    success_url = reverse_lazy("core:activeclub_list")
    success_message = "Klub aktif berhasil dihapus."

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class ActiveClubManageView(ActiveClubBaseMixin, DetailView):
    model = ActiveClub
    template_name = "core/activeclub/manage.html"
    context_object_name = "activeclub"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["students"] = self.object.students.all().order_by("user__first_name")
        context["all_students"] = Student.objects.all().order_by("user__first_name")
        context["total_students"] = self.object.students.count()
        context["breadcrumb_text"] = f"Kelola: {self.object.club.name}"
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        student_id = request.POST.get("student")
        if student_id:
            student = get_object_or_404(Student, pk=student_id)
            if self.object.students.filter(pk=student.pk).exists():
                messages.error(request, "Siswa sudah menjadi anggota klub ini.")
            else:
                self.object.students.add(student)
                messages.success(request, "Siswa berhasil ditambahkan.")
        else:
            messages.error(request, "Pilih siswa yang valid.")
        return redirect("core:activeclub_manage", pk=self.object.pk)


class ClubStudentDeleteView(ActiveClubBaseMixin, SuccessMessageMixin, DeleteView):
    model = None
    success_message = "Siswa berhasil dihapus dari klub."

    def get_success_url(self):
        return reverse_lazy(
            "core:activeclub_manage", kwargs={"pk": self.kwargs["club_pk"]}
        )

    def post(self, request, *args, **kwargs):
        club = get_object_or_404(ActiveClub, pk=kwargs["club_pk"])
        student = get_object_or_404(Student, pk=kwargs["student_pk"])
        club.students.remove(student)
        messages.success(self.request, self.success_message)
        return redirect(self.get_success_url())
