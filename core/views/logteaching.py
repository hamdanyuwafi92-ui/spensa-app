from collections import defaultdict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from core.models import ActiveClass, ActiveSubject, Teacher

from .base import GlobalContextMixin


class LogTeachingView(LoginRequiredMixin, GlobalContextMixin, TemplateView):
    template_name = "core/logteaching.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb_text"] = "Riwayat Mengajar"

        user = self.request.user
        teacher = getattr(user, "teacher", None)

        if not teacher:
            context["data"] = []
            context["total_entries"] = 0
            context["message"] = "Profil guru tidak ditemukan. Hubungi administrator."
            return context

        active_subjects = ActiveSubject.objects.select_related(
            "activeyear__year", "activeyear__semester", "subject"
        ).filter(teacher=teacher)

        if not active_subjects.exists():
            context["data"] = []
            context["total_entries"] = 0
            context["message"] = "Belum ada riwayat mengajar."
            return context

        wali_kelas_map = {}
        for ac in ActiveClass.objects.filter(teacher=teacher).select_related(
            "classroom", "activeyear"
        ):
            wali_kelas_map[ac.activeyear_id] = str(ac.classroom)

        grouped = defaultdict(
            lambda: {
                "subjects": set(),
                "total_classes": 0,
                "semester": "",
                "is_wali": False,
                "classroom": "-",
            }
        )
        for as_ in active_subjects:
            ay = as_.activeyear
            ay_id = ay.id
            grouped[ay_id]["subjects"].add(as_.subject.name)
            grouped[ay_id]["total_classes"] += 1
            grouped[ay_id]["semester"] = ay.semester.name
            grouped[ay_id]["activeyear_name"] = ay.year.name
            if ay_id in wali_kelas_map:
                grouped[ay_id]["is_wali"] = True
                grouped[ay_id]["classroom"] = wali_kelas_map[ay_id]

        data = []
        for ay_id, info in grouped.items():
            data.append(
                {
                    "activeyear": info["activeyear_name"],
                    "semester": info["semester"],
                    "subjects": ", ".join(sorted(info["subjects"])),
                    "subjects_list": sorted(info["subjects"]),
                    "total_classes": info["total_classes"],
                    "is_wali": info["is_wali"],
                    "classroom": info["classroom"],
                }
            )
        data.sort(key=lambda x: x["activeyear"], reverse=True)

        paginator = Paginator(data, 10)
        page = self.request.GET.get("page")
        context["page_obj"] = paginator.get_page(page)
        context["total_entries"] = len(data)
        return context
