from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.views.generic import TemplateView
from xhtml2pdf import pisa

from core.models import (
    ActiveClass,
    ActiveClassStudent,
    ActiveSubject,
    ActiveYear,
    Performance,
    Student,
    Summary,
)
from core.utilities.resources import generate_transcript_pdf

from .base import GlobalContextMixin


class TranscriptBaseMixin(LoginRequiredMixin, GlobalContextMixin):
    def get_teacher_classes(self):
        teacher = getattr(self.request.user, "teacher", None)
        if not teacher:
            return []
        return ActiveSubject.objects.filter(teacher=teacher).select_related(
            "classroom", "activeyear__year", "activeyear__semester"
        )


class TranscriptView(TranscriptBaseMixin, TemplateView):
    template_name = "core/transcript.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb_text"] = "Transkrip Nilai"
        teacher_subjects = self.get_teacher_classes()
        context["subjects"] = teacher_subjects

        classroom_id = self.request.GET.get("classroom_id")
        year_id = self.request.GET.get("year_id")
        if classroom_id and year_id:
            try:
                active_class = ActiveClass.objects.get(
                    classroom_id=classroom_id, activeyear_id=year_id
                )
            except ActiveClass.DoesNotExist:
                context["message"] = "Kelas tidak ditemukan."
                return context

            students = (
                ActiveClassStudent.objects.filter(activeclass=active_class)
                .select_related("student")
                .order_by("student__user__first_name")
            )

            student_data = []
            for acs in students:
                summaries = Summary.objects.filter(
                    student=acs, subject__activeyear_id=year_id
                ).select_related("subject__subject")
                avg = (
                    sum(s.final_score for s in summaries) / summaries.count()
                    if summaries
                    else 0
                )
                student_data.append(
                    {
                        "id": acs.student.id,
                        "nisn": acs.student.nisn,
                        "name": acs.student.fullname(),
                        "classroom": str(active_class.classroom),
                        "average": round(avg, 2),
                    }
                )
            context["students"] = student_data
        return context


class TranscriptDownloadView(TranscriptBaseMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        student_id = kwargs.get("student_id")
        year_id = request.GET.get("year_id")
        if not student_id or not year_id:
            messages.error(request, "Parameter tidak lengkap.")
            return redirect("core:transcript")

        student = get_object_or_404(Student, pk=student_id)
        active_year = get_object_or_404(ActiveYear, pk=year_id)

        acs = get_object_or_404(
            ActiveClassStudent,
            student=student,
            activeclass__activeyear=active_year,
        )

        summaries = Summary.objects.filter(
            student=acs, subject__activeyear=active_year
        ).select_related("subject__subject", "student")

        performances = Performance.objects.filter(
            student=student, active_club__activeyear=active_year
        ).select_related("active_club__club")

        context = generate_transcript_pdf(
            student,
            acs,
            summaries,
            performances,
            active_year.year.name,
            active_year.semester.name,
        )
        html = render_to_string("core/transcript/pdf.html", context)
        response = HttpResponse(content_type="application/pdf")
        filename = f"transkrip_{student.nisn}_{active_year.year.name}_{active_year.semester.name}.pdf"
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            messages.error(request, "Gagal menghasilkan PDF.")
            return redirect("core:transcript")
        return response


class TranscriptDownloadAllView(TranscriptBaseMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        classroom_id = request.GET.get("classroom_id")
        year_id = request.GET.get("year_id")
        if not classroom_id or not year_id:
            messages.error(request, "Parameter tidak lengkap.")
            return redirect("core:transcript")

        try:
            active_class = ActiveClass.objects.get(
                classroom_id=classroom_id, activeyear_id=year_id
            )
        except ActiveClass.DoesNotExist:
            messages.error(request, "Kelas tidak ditemukan.")
            return redirect("core:transcript")

        active_year = active_class.activeyear
        students = (
            ActiveClassStudent.objects.filter(activeclass=active_class)
            .select_related("student")
            .order_by("student__user__first_name")
        )

        # Generate single PDF with all pages
        all_pages_html = ""
        for acs in students:
            student = acs.student
            summaries = Summary.objects.filter(
                student=acs, subject__activeyear=active_year
            ).select_related("subject__subject", "student")
            performances = Performance.objects.filter(
                student=student, active_club__activeyear=active_year
            ).select_related("active_club__club")
            context = generate_transcript_pdf(
                student,
                acs,
                summaries,
                performances,
                active_year.year.name,
                active_year.semester.name,
            )
            page_html = render_to_string("core/transcript/pdf.html", context)
            all_pages_html += (
                page_html + '<div style="page-break-after: always;"></div>'
            )

        # Wrap all pages in a minimal HTML document
        final_html = render_to_string("core/transcript/pdf_all.html", {"all_pages_html": all_pages_html})

        response = HttpResponse(content_type="application/pdf")
        filename = (
            f"transkrip_all_{active_year.year.name}_{active_year.semester.name}.pdf"
        )
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        pisa_status = pisa.CreatePDF(final_html, dest=response)
        if pisa_status.err:
            messages.error(request, "Gagal menghasilkan PDF.")
            return redirect("core:transcript")
        return response
