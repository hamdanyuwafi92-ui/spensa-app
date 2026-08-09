from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, UpdateView, DeleteView
from django.views.generic.edit import CreateView

from core.forms.activeclass import ActiveClassForm, AddStudentForm
from core.models import (
    ActiveClass,
    ActiveClassStudent,
    ActiveYear,
    Classroom,
    Student,
    Teacher,
)
from .base import BaseAccessMixin, ModalFormMixin


class ActiveClassContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb_text"] = "Kelas Aktif"
        return context


class ActiveClassBaseMixin(BaseAccessMixin, ActiveClassContextMixin):
    pass


class ActiveClassListView(ActiveClassBaseMixin, ListView):
    template_name = "core/activeclass.html"
    context_object_name = "active_classes"
    paginate_by = 10

    def get_queryset(self):
        return ActiveClass.objects.select_related(
            "activeyear", "classroom", "teacher"
        ).order_by("-id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_mode"] = "list"
        active_year = ActiveYear.get_active()
        context["active_year"] = active_year
        context["classrooms"] = Classroom.objects.all()
        context["teachers"] = Teacher.objects.filter(
            job__in=["Guru", "Developer", "Administrator", "Agent"]
        )
        if not active_year:
            messages.warning(
                self.request,
                "Tidak ada tahun ajaran aktif. Silakan aktifkan satu tahun ajaran terlebih dahulu.",
            )
        return context


class ActiveClassCreateView(
    ActiveClassBaseMixin, ModalFormMixin, SuccessMessageMixin, CreateView
):
    model = ActiveClass
    form_class = ActiveClassForm
    form_type = "activeclass"
    template_name = "core/activeclass.html"
    success_url = reverse_lazy("core:activeclass_list")
    success_message = "Kelas aktif berhasil ditambahkan."

    def dispatch(self, request, *args, **kwargs):
        active_year = ActiveYear.get_active()
        if not active_year:
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
        context["classrooms"] = Classroom.objects.all()
        context["teachers"] = Teacher.objects.filter(
            job__in=["Guru", "Developer", "Administrator", "Agent"]
        )
        return context


class ActiveClassUpdateView(
    ActiveClassBaseMixin, ModalFormMixin, SuccessMessageMixin, UpdateView
):
    model = ActiveClass
    form_class = ActiveClassForm
    form_type = "activeclass"
    template_name = "core/activeclass.html"
    success_url = reverse_lazy("core:activeclass_list")
    success_message = "Kelas aktif berhasil diperbarui."

    def dispatch(self, request, *args, **kwargs):
        active_year = ActiveYear.get_active()
        if not active_year:
            messages.warning(
                request,
                "Tidak ada tahun ajaran aktif. Silakan aktifkan satu tahun ajaran terlebih dahulu.",
            )
            return redirect("core:year_manage")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_year"] = ActiveYear.get_active()
        context["classrooms"] = Classroom.objects.all()
        context["teachers"] = Teacher.objects.filter(
            job__in=["Guru", "Developer", "Administrator", "Agent"]
        )
        return context


class ActiveClassDeleteView(ActiveClassBaseMixin, SuccessMessageMixin, DeleteView):
    model = ActiveClass
    template_name = "core/activeclass.html"
    success_url = reverse_lazy("core:activeclass_list")
    success_message = "Kelas aktif berhasil dihapus."

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class ActiveClassManageView(ActiveClassBaseMixin, DetailView):
    model = ActiveClass
    template_name = "core/activeclass/manage.html"
    context_object_name = "activeclass"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student_list = Student.objects.filter(
            activeclassstudent__activeclass=self.object
        ).order_by("id")
        paginator = Paginator(student_list, 10)
        page = self.request.GET.get("page")
        context["students"] = paginator.get_page(page)
        context["add_student_form"] = AddStudentForm()
        context["total_students"] = student_list.count()
        all_students_qs = Student.objects.all()
        all_students_sorted = sorted(all_students_qs, key=lambda s: s.fullname())
        context["all_students"] = all_students_sorted
        context["breadcrumb_text"] = f"Kelola: {self.object.classroom}"
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = AddStudentForm(request.POST)
        if form.is_valid():
            student = form.cleaned_data["student"]
            try:
                ActiveClassStudent.objects.create(
                    activeclass=self.object, student=student
                )
                messages.success(request, "Siswa berhasil ditambahkan.")
            except ValidationError as e:
                messages.error(request, e.messages[0])
            return redirect("core:activeclass_manage", pk=self.object.pk)
        messages.error(request, "Pilih siswa yang valid.")
        return redirect("core:activeclass_manage", pk=self.object.pk)


class StudentDeleteView(ActiveClassBaseMixin, SuccessMessageMixin, DeleteView):
    model = ActiveClassStudent
    success_message = "Siswa berhasil dihapus dari kelas."

    def get_success_url(self):
        return reverse_lazy(
            "core:activeclass_manage", kwargs={"pk": self.object.activeclass.pk}
        )

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)
