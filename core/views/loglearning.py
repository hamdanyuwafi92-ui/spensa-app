from collections import defaultdict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from core.models import (
    ActiveClassStudent,
    ActiveYear,
    Formative,
    Performance,
    Summative,
    Summary,
)

from .base import GlobalContextMixin


class LogLearningBaseMixin(LoginRequiredMixin, GlobalContextMixin):
    def get_student(self):
        user = self.request.user
        return getattr(user, "student", None)


class LogLearningListView(LogLearningBaseMixin, TemplateView):
    template_name = "core/loglearning.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb_text"] = "Riwayat Nilai"
        student = self.get_student()
        if not student:
            context["entries"] = []
            context["message"] = "Profil siswa tidak ditemukan."
            return context

        summaries = (
            Summary.objects.filter(student__student=student)
            .select_related(
                "subject__activeyear__year", "subject__activeyear__semester"
            )
            .order_by("subject__activeyear")
        )

        year_groups = defaultdict(list)
        for s in summaries:
            ay = s.subject.activeyear
            year_groups[ay.id].append(s)

        entries = []
        for ay_id, items in year_groups.items():
            avg_final = sum(item.final_score for item in items) / len(items)
            ay = items[0].subject.activeyear
            acs = (
                ActiveClassStudent.objects.filter(
                    student=student,
                    activeclass__activeyear_id=ay_id,
                )
                .select_related("activeclass__classroom")
                .first()
            )
            classroom = str(acs.activeclass.classroom) if acs else "-"
            entries.append(
                {
                    "ay_id": ay_id,
                    "activeyear": ay.year.name,
                    "semester": ay.semester.name,
                    "average_raport": round(avg_final, 2),
                    "total_subjects": len(items),
                    "classroom": classroom,
                }
            )
        entries.sort(key=lambda x: x["activeyear"], reverse=True)
        context["entries"] = entries
        return context


class LogLearningDetailView(LogLearningBaseMixin, TemplateView):
    template_name = "core/loglearning/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb_text"] = "Detail Nilai"
        student = self.get_student()
        if not student:
            context["rows"] = []
            context["message"] = "Profil siswa tidak ditemukan."
            return context

        ay_id = self.request.GET.get("year_id")
        if not ay_id:
            context["message"] = "Parameter tahun tidak diberikan."
            return context

        active_year = (
            ActiveYear.objects.filter(pk=ay_id)
            .select_related("year", "semester")
            .first()
        )
        if not active_year:
            context["message"] = "Tahun ajaran tidak ditemukan."
            return context

        acs = (
            ActiveClassStudent.objects.filter(
                student=student,
                activeclass__activeyear=active_year,
            )
            .select_related("activeclass__classroom")
            .first()
        )
        context["student_class"] = str(acs.activeclass.classroom) if acs else "-"

        summaries = Summary.objects.filter(
            student__student=student,
            subject__activeyear=active_year,
        ).select_related("subject__subject", "student__activeclass__classroom")

        rows = []
        for summ in summaries:
            subject = summ.subject
            formatives = Formative.objects.filter(
                teacher=subject, student=summ.student
            ).order_by("type")
            formative_scores = {f.type: f.score for f in formatives}
            summatif = Summative.objects.filter(
                teacher=subject, student=summ.student
            ).first()
            summatif_score = summatif.score if summatif else 0

            performances = Performance.objects.filter(
                student=student, active_club__activeyear=active_year
            )
            club_scores = ", ".join(str(p.score) for p in performances) or "-"
            descriptions = (
                ", ".join(p.description for p in performances if p.description) or "-"
            )

            row = {
                "subject_name": subject.subject.name,
                "f1": formative_scores.get("F1", 0),
                "f2": formative_scores.get("F2", 0),
                "f3": formative_scores.get("F3", 0),
                "f4": formative_scores.get("F4", 0),
                "f5": formative_scores.get("F5", 0),
                "sumatif": summatif_score,
                "avg_formatif": summ.formatif_score,
                "final_score": summ.final_score,
                "club_scores": club_scores,
                "description": descriptions,
            }
            rows.append(row)

        context["rows"] = rows
        context["active_year"] = active_year
        return context
