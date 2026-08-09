from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, UpdateView, DeleteView
from django.views.generic.edit import CreateView

from core.forms.teacher import TeacherForm
from core.models import Teacher, Student
from .base import BaseAccessMixin

User = get_user_model()


class TeacherContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_teachers"] = Teacher.objects.count()
        context["total_students"] = Student.objects.count()
        context["total_administrator"] = Teacher.objects.filter(
            job="Administrator"
        ).count()
        context["total_staff"] = Teacher.objects.filter(job="Agent").count()
        context["total_guru"] = Teacher.objects.filter(job="Guru").count()
        context["breadcrumb_text"] = "Guru"
        return context


class TeacherBaseMixin(BaseAccessMixin, TeacherContextMixin):
    pass


class TeacherListView(TeacherBaseMixin, ListView):
    template_name = "core/teacher.html"
    context_object_name = "teachers"
    paginate_by = 10

    def get_queryset(self):
        return Teacher.objects.select_related("user").order_by("user__first_name")


class TeacherCreateView(TeacherBaseMixin, SuccessMessageMixin, CreateView):
    model = Teacher
    form_class = TeacherForm
    template_name = "core/teacher/teacher_form.html"
    success_url = reverse_lazy("core:teacher_list")
    success_message = "Data guru berhasil ditambahkan."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Tambah Guru Baru"
        return context


class TeacherUpdateView(TeacherBaseMixin, SuccessMessageMixin, UpdateView):
    model = Teacher
    form_class = TeacherForm
    template_name = "core/teacher/teacher_form.html"
    success_url = reverse_lazy("core:teacher_list")
    success_message = "Data guru berhasil diperbarui."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Edit Guru"
        return context


class TeacherDeleteView(TeacherBaseMixin, SuccessMessageMixin, DeleteView):
    model = Teacher
    template_name = "core/teacher.html"
    success_url = reverse_lazy("core:teacher_list")
    success_message = "Data guru berhasil dihapus."

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class TeacherDetailView(TeacherBaseMixin, DetailView):
    model = Teacher
    template_name = "core/teacher/teacher_detail.html"
    context_object_name = "teacher"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb_text"] = f"Detail: {self.object.fullname()}"
        return context


class TeacherResetPasswordView(TeacherBaseMixin, DetailView):
    model = Teacher

    def post(self, request, *args, **kwargs):
        teacher = self.get_object()
        if teacher.user:
            teacher.user.password = make_password("guruoke123")
            teacher.user.save()
            messages.success(
                request,
                f"Password untuk {teacher.fullname()} telah direset ke 'guruoke123'.",
            )
        else:
            messages.error(request, "Guru belum memiliki akun pengguna.")
        return redirect("core:teacher_list")
