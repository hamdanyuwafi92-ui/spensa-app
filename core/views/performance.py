from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from core.models import ActiveClub, Performance, Student

from .base import GlobalContextMixin


class PerformanceView(LoginRequiredMixin, GlobalContextMixin, TemplateView):
    template_name = "core/performance.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb_text"] = "Penilaian Ekstrakurikuler"
        teacher = getattr(self.request.user, "teacher", None)
        if not teacher:
            context["message"] = "Profil pelatih tidak ditemukan."
            return context

        clubs = ActiveClub.objects.filter(teacher=teacher).select_related(
            "club", "activeyear"
        )
        context["clubs"] = clubs

        club_id = self.request.GET.get("club_id")
        if club_id:
            try:
                selected_club = clubs.get(pk=club_id)
            except ActiveClub.DoesNotExist:
                context["message"] = "Klub tidak valid."
                return context

            context["selected_club"] = selected_club
            students = selected_club.students.all().order_by("user__first_name")

            performances = Performance.objects.filter(
                active_club=selected_club,
                student__in=students,
            )
            scores = {p.student_id: p for p in performances}

            student_data = []
            for student in students:
                sid = student.id
                perf = scores.get(sid)
                student_data.append(
                    {
                        "id": sid,
                        "student_nisn": student.nisn,
                        "student_name": student.fullname(),
                        "student_gender": student.gender,
                        "score": perf.score if perf else 0,
                        "description": (
                            perf.description if perf else "Silahkan Isi Deskripsi"
                        ),
                    }
                )
            context["students"] = student_data
        return context

    def post(self, request, *args, **kwargs):
        teacher = getattr(request.user, "teacher", None)
        if not teacher:
            messages.error(request, "Profil pelatih tidak ditemukan.")
            return redirect("core:performance")

        club_id = request.POST.get("club_id")
        if not club_id:
            messages.error(request, "Klub tidak dipilih.")
            return redirect("core:performance")

        try:
            selected_club = ActiveClub.objects.get(pk=club_id, teacher=teacher)
        except ActiveClub.DoesNotExist:
            messages.error(request, "Klub tidak valid.")
            return redirect("core:performance")

        for key, value in request.POST.items():
            if key.startswith("score_"):
                student_id = key[6:]
                try:
                    student = Student.objects.get(pk=student_id)
                except Student.DoesNotExist:
                    continue
                try:
                    score = float(value or 0)
                except ValueError:
                    score = 0
                description_key = f"desc_{student_id}"
                description = request.POST.get(
                    description_key, "Silahkan Isi Deskripsi"
                )
                Performance.objects.update_or_create(
                    teacher=teacher,
                    active_club=selected_club,
                    student=student,
                    defaults={"score": score, "description": description},
                )

        messages.success(request, "Nilai ekstrakurikuler berhasil disimpan.")
        return redirect(f"/core/performance/?club_id={club_id}")
