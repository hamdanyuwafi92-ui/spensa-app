from django.contrib import messages
from django.views.generic import TemplateView
from core.utilities.sync import sync_all
from .base import BaseAccessMixin, GlobalContextMixin


class SyncView(BaseAccessMixin, GlobalContextMixin, TemplateView):
    template_name = "core/config.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb_text"] = "Pengaturan"
        context["active_tab"] = "sync"
        return context

    def post(self, request, *args, **kwargs):
        counts = sync_all()
        total = counts["formatif"] + counts["summatif"] + counts["performance"]
        msg = (
            f"Sinkronisasi selesai. Formatif: {counts['formatif']}, "
            f"Sumatif: {counts['summatif']}, Performance: {counts['performance']}. "
            f"({counts['clubs_processed']} klub diproses, {counts['students_total']} total siswa)"
        )
        if total == 0:
            messages.info(request, "Semua data sudah lengkap. Tidak ada penambahan.")
        else:
            messages.success(request, msg)
        return self.get(request, *args, **kwargs)
