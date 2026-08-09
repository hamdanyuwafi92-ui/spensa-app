from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView
from core.models import (
    Year,
    Semester,
    Classroom,
    Subject,
    Club,
    Teacher,
    Student,
)
from core.utilities.backup import (
    backup_model_to_excel,
    restore_model_from_excel,
    restore_teacher_from_excel,
    restore_student_from_excel,
)
from .base import BaseAccessMixin, GlobalContextMixin

BACKUP_MODELS = {
    "Year": Year,
    "Semester": Semester,
    "Classroom": Classroom,
    "Subject": Subject,
    "Club": Club,
    "Teacher": Teacher,
    "Student": Student,
}


class BackupView(BaseAccessMixin, GlobalContextMixin, TemplateView):
    template_name = "core/config.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb_text"] = "Pengaturan"
        context["active_tab"] = "backup"

        models_info = []
        for name, model_cls in BACKUP_MODELS.items():
            models_info.append({"name": name, "count": model_cls.objects.count()})
        context["models"] = models_info

        return context

    def post(self, request, *args, **kwargs):
        action = request.POST.get("action")
        model_name = request.POST.get("model")

        if action == "backup":
            model_class = BACKUP_MODELS.get(model_name)
            if not model_class:
                messages.error(request, "Model tidak valid.")
                return redirect("core:backup")

            extra_fields = []
            if model_class == Teacher:
                extra_fields = ["user__first_name", "user__last_name", "user__email"]
            elif model_class == Student:
                extra_fields = ["user__first_name", "user__last_name", "user__email"]

            excel_file = backup_model_to_excel(model_class, extra_fields=extra_fields)
            response = HttpResponse(
                excel_file,
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
            response["Content-Disposition"] = (
                f'attachment; filename="{model_name}_backup.xlsx"'
            )
            return response

        elif action == "restore":
            model_class = BACKUP_MODELS.get(model_name)
            if not model_class:
                messages.error(request, "Model tidak valid.")
                return redirect("core:backup")

            uploaded_file = request.FILES.get("file")
            if not uploaded_file:
                messages.error(request, "File tidak ditemukan.")
                return redirect("core:backup")

            try:
                if model_class == Teacher:
                    restore_teacher_from_excel(uploaded_file, request.user)
                    messages.success(
                        request,
                        "Data Teacher berhasil direstore dengan akun user baru.",
                    )
                elif model_class == Student:
                    restore_student_from_excel(uploaded_file, request.user)
                    messages.success(
                        request,
                        "Data Student berhasil direstore dengan akun user baru.",
                    )
                else:
                    restore_model_from_excel(
                        model_class, uploaded_file, user=request.user
                    )
                    messages.success(request, f"Data {model_name} berhasil direstore.")
            except Exception as e:
                messages.error(request, f"Gagal restore: {e}")

            return redirect("core:backup")

        return redirect("core:backup")
