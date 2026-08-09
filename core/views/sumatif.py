from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from core.models import ActiveSubject, Summative, ActiveClassStudent

from .base import GlobalContextMixin


class SumatifView(LoginRequiredMixin, GlobalContextMixin, TemplateView):
    template_name = "core/sumatif.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb_text"] = "Penilaian Sumatif"
        teacher = getattr(self.request.user, "teacher", None)
        if not teacher:
            context["message"] = "Profil guru tidak ditemukan."
            return context

        # Daftar mapel yang diampu
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

            # Ambil nilai sumatif yang sudah ada
            sumatif_qs = Summative.objects.filter(
                teacher=selected_subject,
                student__in=students,
            )
            scores = {s.student_id: s.score for s in sumatif_qs}

            student_data = []
            for student in students:
                sid = student.id
                student_data.append(
                    {
                        "id": sid,
                        "student_nisn": student.student.nisn,
                        "student_name": student.student.fullname(),
                        "student_gender": student.student.gender,
                        "score": scores.get(sid, 0),
                    }
                )
            context["students"] = student_data
        return context

    def post(self, request, *args, **kwargs):
        teacher = getattr(request.user, "teacher", None)
        if not teacher:
            messages.error(request, "Profil guru tidak ditemukan.")
            return redirect("core:sumatif")

        subject_id = request.POST.get("subject_id")
        if not subject_id:
            messages.error(request, "Mata pelajaran tidak dipilih.")
            return redirect("core:sumatif")

        try:
            selected_subject = ActiveSubject.objects.get(pk=subject_id, teacher=teacher)
        except ActiveSubject.DoesNotExist:
            messages.error(request, "Mata pelajaran tidak valid.")
            return redirect("core:sumatif")

        for key, value in request.POST.items():
            if key.startswith("score_"):
                student_id = key[6:]  # setelah "score_"
                try:
                    student = ActiveClassStudent.objects.get(pk=student_id)
                except ActiveClassStudent.DoesNotExist:
                    continue
                try:
                    score = float(value or 0)
                except ValueError:
                    score = 0
                Summative.objects.update_or_create(
                    teacher=selected_subject,
                    student=student,
                    defaults={"score": score},
                )

        messages.success(request, "Nilai sumatif berhasil disimpan.")
        return redirect(f"/core/sumatif/?subject_id={subject_id}")
