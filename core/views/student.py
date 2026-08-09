from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, UpdateView, DeleteView
from django.views.generic.edit import CreateView

from core.forms.student import StudentForm
from core.models import Student
from .base import BaseAccessMixin

User = get_user_model()


class StudentContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_students"] = Student.objects.count()
        context["total_aktif"] = Student.objects.filter(status="Aktif").count()
        context["total_lulus"] = Student.objects.filter(status="Lulus").count()
        context["total_keluar"] = Student.objects.filter(status="Keluar").count()
        context["breadcrumb_text"] = "Siswa"
        return context


class StudentBaseMixin(BaseAccessMixin, StudentContextMixin):
    pass


class StudentListView(StudentBaseMixin, ListView):
    template_name = "core/student.html"
    context_object_name = "students"
    paginate_by = 10

    def get_queryset(self):
        return Student.objects.select_related("user").order_by("user__first_name")


class StudentCreateView(StudentBaseMixin, SuccessMessageMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = "core/student/student_form.html"
    success_url = reverse_lazy("core:student_list")
    success_message = "Data siswa berhasil ditambahkan."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Tambah Siswa Baru"
        return context


class StudentUpdateView(StudentBaseMixin, SuccessMessageMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = "core/student/student_form.html"
    success_url = reverse_lazy("core:student_list")
    success_message = "Data siswa berhasil diperbarui."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Edit Siswa"
        return context


class StudentDeleteView(StudentBaseMixin, SuccessMessageMixin, DeleteView):
    model = Student
    template_name = "core/student.html"
    success_url = reverse_lazy("core:student_list")
    success_message = "Data siswa berhasil dihapus."

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class StudentDetailView(StudentBaseMixin, DetailView):
    model = Student
    template_name = "core/student/student_detail.html"
    context_object_name = "student"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb_text"] = f"Detail: {self.object.fullname()}"
        return context


class StudentResetPasswordView(StudentBaseMixin, DetailView):
    model = Student

    def post(self, request, *args, **kwargs):
        student = self.get_object()
        if student.user:
            student.user.password = make_password("siswaoke123")
            student.user.save()
            messages.success(
                request,
                f"Password untuk {student.fullname()} telah direset ke 'siswaoke123'.",
            )
        else:
            messages.error(request, "Siswa belum memiliki akun pengguna.")
        return redirect("core:student_list")
