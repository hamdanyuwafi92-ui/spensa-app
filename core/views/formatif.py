from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from core.models import ActiveSubject, Formative, ActiveClassStudent

from .base import GlobalContextMixin


class FormatifView(LoginRequiredMixin, GlobalContextMixin, TemplateView):
    template_name = "core/formatif.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb_text"] = "Penilaian Formatif"
        teacher = getattr(self.request.user, "teacher", None)
        if not teacher:
            context["message"] = "Profil guru tidak ditemukan."
            return context

        subjects = ActiveSubject.objects.filter(teacher=teacher).select_related(
            "subject", "classroom", "activeyear"
        )
        context["subjects"] = subjects

        subject_id = self.request.GET.get("subject_id")
        if subject_id:
            try:
                selected_subject = subjects.get(pk=subject_id)
            except ActiveSubject.DoesNotExist:
                context["message"] = "Mata pelajaran tidak valid."
                return context

            context["selected_subject"] = selected_subject
            students = (
                ActiveClassStudent.objects.filter(
                    activeclass__classroom=selected_subject.classroom,
                    activeclass__activeyear=selected_subject.activeyear,
                )
                .select_related("student")
                .order_by("student__user__first_name")
            )

            formatives = Formative.objects.filter(
                teacher=selected_subject,
                student__in=students,
            ).order_by("student", "type")

            scores = {}
            for f in formatives:
                if f.student_id not in scores:
                    scores[f.student_id] = {}
                scores[f.student_id][f.type] = f.score

            student_data = []
            for student in students:
                sid = student.id
                student_data.append(
                    {
                        "id": sid,
                        "student_nisn": student.student.nisn,
                        "student_name": student.student.fullname(),
                        "student_gender": student.student.gender,
                        "p1": scores.get(sid, {}).get("F1", 0),
                        "p2": scores.get(sid, {}).get("F2", 0),
                        "p3": scores.get(sid, {}).get("F3", 0),
                        "p4": scores.get(sid, {}).get("F4", 0),
                        "p5": scores.get(sid, {}).get("F5", 0),
                    }
                )
            context["students"] = student_data
        return context

    def post(self, request, *args, **kwargs):
        teacher = getattr(request.user, "teacher", None)
        if not teacher:
            messages.error(request, "Profil guru tidak ditemukan.")
            return redirect("core:formatif")

        subject_id = request.POST.get("subject_id")
        if not subject_id:
            messages.error(request, "Mata pelajaran tidak dipilih.")
            return redirect("core:formatif")

        try:
            selected_subject = ActiveSubject.objects.get(pk=subject_id, teacher=teacher)
        except ActiveSubject.DoesNotExist:
            messages.error(request, "Mata pelajaran tidak valid.")
            return redirect("core:formatif")

        for key, value in request.POST.items():
            if key.startswith("score_"):
                parts = key.split("_")
                if len(parts) != 3:
                    continue
                student_id = parts[1]
                score_type = parts[2]
                try:
                    student = ActiveClassStudent.objects.get(pk=student_id)
                except ActiveClassStudent.DoesNotExist:
                    continue
                if score_type not in ["F1", "F2", "F3", "F4", "F5"]:
                    continue
                try:
                    score = float(value or 0)
                except ValueError:
                    score = 0
                Formative.objects.update_or_create(
                    teacher=selected_subject,
                    student=student,
                    type=score_type,
                    defaults={"score": score},
                )

        messages.success(request, "Nilai formatif berhasil disimpan.")
        return redirect(f"/core/formatif/?subject_id={subject_id}")
