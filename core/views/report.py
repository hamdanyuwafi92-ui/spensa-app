from django.db.models import Count, Q
from django.views.generic import TemplateView
from core.models import (
    ActiveClass,
    ActiveClassStudent,
    ActiveSubject,
    ActiveClub,
    Student,
    Teacher,
)
from core.utilities.access import DevAdminAccessMixin
from .base import GlobalContextMixin


class ReportView(DevAdminAccessMixin, GlobalContextMixin, TemplateView):
    template_name = "core/report.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb_text"] = "Report & Analytic"

        total_students = Student.objects.count()
        students_in_class = (
            ActiveClassStudent.objects.values("student").distinct().count()
        )
        context["students_no_class"] = total_students - students_in_class

        guru_job = Teacher.objects.filter(job="Guru")
        guru_wali_ids = (
            ActiveClass.objects.filter(teacher__in=guru_job)
            .values_list("teacher_id", flat=True)
            .distinct()
        )
        context["guru_not_wali"] = guru_job.exclude(id__in=guru_wali_ids).count()

        guru_active_subject_ids = (
            ActiveSubject.objects.filter(teacher__in=guru_job)
            .values_list("teacher_id", flat=True)
            .distinct()
        )
        context["guru_no_subject"] = guru_job.exclude(
            id__in=guru_active_subject_ids
        ).count()

        staff_job = Teacher.objects.filter(job="Agent")
        staff_active_club_ids = (
            ActiveClub.objects.filter(teacher__in=staff_job)
            .values_list("teacher_id", flat=True)
            .distinct()
        )
        context["staff_no_schedule"] = staff_job.exclude(
            id__in=staff_active_club_ids
        ).count()

        active_classes = (
            ActiveClass.objects.select_related("classroom", "teacher__user")
            .annotate(
                total_students=Count("students"),
                male_students=Count("students", filter=Q(students__gender="Laki-laki")),
                female_students=Count(
                    "students", filter=Q(students__gender="Perempuan")
                ),
                active_students=Count(
                    "students", filter=Q(students__user__is_active=True)
                ),
            )
            .order_by("classroom__mainclassroom", "classroom__name")
        )
        context["active_classes"] = active_classes

        active_subjects = (
            ActiveSubject.objects.select_related(
                "subject", "teacher__user", "classroom"
            )
            .annotate(
                total_jenjang=Count("classroom__mainclassroom", distinct=True),
                total_kelas=Count("classroom", distinct=True),
            )
            .order_by("subject__name")
        )
        context["active_subjects"] = active_subjects

        active_clubs = (
            ActiveClub.objects.select_related("club", "teacher__user")
            .annotate(
                total_students=Count("students"),
            )
            .order_by("club__name")
        )
        context["active_clubs"] = active_clubs

        return context
