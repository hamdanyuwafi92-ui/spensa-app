from collections import defaultdict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from core.models import ActiveClub

from .base import GlobalContextMixin


class LogAgentView(LoginRequiredMixin, GlobalContextMixin, TemplateView):
    template_name = "core/logagent.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb_text"] = "Riwayat Pelatih"
        teacher = getattr(self.request.user, "teacher", None)
        if not teacher:
            context["data"] = []
            context["total_entries"] = 0
            context["message"] = "Profil pelatih tidak ditemukan."
            return context

        clubs = (
            ActiveClub.objects.filter(teacher=teacher)
            .select_related("activeyear__year", "activeyear__semester", "club")
            .prefetch_related("students")
        )

        grouped = defaultdict(lambda: {"total_students": 0})
        for club in clubs:
            ay = club.activeyear
            key = ay.id
            grouped[key]["activeyear"] = ay.year.name
            grouped[key]["semester"] = ay.semester.name
            grouped[key]["club"] = club.club.name
            grouped[key]["total_students"] += club.students.count()

        data = []
        for ay_id, info in grouped.items():
            data.append(
                {
                    "activeyear": info["activeyear"],
                    "semester": info["semester"],
                    "club": info["club"],
                    "total_students": info["total_students"],
                }
            )
        data.sort(key=lambda x: x["activeyear"], reverse=True)
        context["data"] = data
        context["total_entries"] = len(data)
        return context
