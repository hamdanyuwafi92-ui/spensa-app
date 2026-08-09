from django.db.models import Avg, Count, Q

from core.models import (
    ActiveClass,
    ActiveClassStudent,
    ActiveClub,
    ActiveSubject,
    ActiveYear,
    Album,
    Article,
    Page,
    Performance,
    Student,
    Summary,
    Teacher,
    Comment,
)

from .base import BaseView


class IndexView(BaseView):
    template_name = "core/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        job = "guru"
        if user.is_superuser:
            job = "developer"
        elif hasattr(user, "teacher"):
            teacher = user.teacher
            job_map = {
                "Developer": "developer",
                "Administrator": "administrator",
                "Agent": "staff",
                "Guru": "guru",
            }
            job = job_map.get(teacher.job, "guru")
        elif hasattr(user, "student"):
            job = "siswa"
        context["dashboard_template"] = f"core/dashboard/{job}.html"
        context["breadcrumb_text"] = "Dashboard"

        context["total_teachers"] = Teacher.objects.count()
        context["total_students"] = Student.objects.count()
        context["total_articles"] = Article.objects.count()
        context["total_pages"] = Page.objects.count()
        context["total_albums"] = Album.objects.count()
        context["recent_comments"] = Comment.objects.select_related("article").order_by(
            "-created_at"
        )[:10]
        active_year = ActiveYear.get_active()
        context["active_year"] = active_year
        context["active_classes_count"] = (
            ActiveClass.objects.filter(activeyear=active_year).count()
            if active_year
            else 0
        )
        context["active_clubs_count"] = (
            ActiveClub.objects.filter(activeyear=active_year).count()
            if active_year
            else 0
        )

        if job == "staff" and hasattr(user, "teacher"):
            teacher = user.teacher
            context["staff_clubs_count"] = ActiveClub.objects.filter(
                teacher=teacher, activeyear=active_year
            ).count()
            context["staff_students_count"] = (
                Student.objects.filter(activeclub__teacher=teacher).distinct().count()
            )
            context["staff_pending_performance"] = (
                ActiveClub.objects.filter(teacher=teacher, activeyear=active_year)
                .annotate(
                    done=Count(
                        "performances",
                        filter=Q(performances__score__gt=0),
                    )
                )
                .filter(done=0)
                .count()
            )

        if job == "guru" and hasattr(user, "teacher"):
            teacher = user.teacher
            context["guru_classes_count"] = (
                ActiveSubject.objects.filter(teacher=teacher, activeyear=active_year)
                .values("classroom")
                .distinct()
                .count()
            )
            context["guru_subjects_count"] = (
                ActiveSubject.objects.filter(teacher=teacher, activeyear=active_year)
                .values("subject")
                .distinct()
                .count()
            )
            formatives_done = (
                ActiveSubject.objects.filter(teacher=teacher, activeyear=active_year)
                .annotate(
                    done=Count(
                        "formatives",
                        filter=Q(formatives__score__gt=0),
                    )
                )
                .filter(done=0)
                .count()
            )
            sumatives_done = (
                ActiveSubject.objects.filter(teacher=teacher, activeyear=active_year)
                .annotate(
                    done=Count(
                        "summatives",
                        filter=Q(summatives__score__gt=0),
                    )
                )
                .filter(done=0)
                .count()
            )
            context["guru_pending_tasks"] = formatives_done + sumatives_done

        if job == "siswa" and hasattr(user, "student"):
            student = user.student
            summaries = Summary.objects.filter(
                student__student=student, subject__activeyear=active_year
            )
            context["siswa_subject_count"] = summaries.count()
            context["siswa_avg_score"] = (
                summaries.aggregate(avg=Avg("final_score"))["avg"] or 0
            )
            context["siswa_clubs_count"] = Performance.objects.filter(
                student=student, active_club__activeyear=active_year
            ).count()

        return context
