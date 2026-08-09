from io import BytesIO
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from core.models import School, Summary, Formative, Summative, Performance


def render_to_pdf(template_src, context_dict):
    result = BytesIO()
    html = render_to_string(template_src, context_dict)
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type="application/pdf")
    return None


def generate_transcript_pdf(
    student, active_class_student, summaries, performances, year_name, semester_name
):
    school = School.get_solo()
    rows = []
    for summary in summaries:
        formative_qs = Formative.objects.filter(
            teacher=summary.subject, student=summary.student
        ).order_by("type")
        p_scores = {f.type: f.score for f in formative_qs}
        sumatif = Summative.objects.filter(
            teacher=summary.subject, student=summary.student
        ).first()
        sumatif_score = sumatif.score if sumatif else 0
        rows.append(
            {
                "subject_name": summary.subject.subject.name,
                "f1": p_scores.get("F1", 0),
                "f2": p_scores.get("F2", 0),
                "f3": p_scores.get("F3", 0),
                "f4": p_scores.get("F4", 0),
                "f5": p_scores.get("F5", 0),
                "sumatif": sumatif_score,
                "avg_formatif": summary.formatif_score,
                "final_score": summary.final_score,
            }
        )

    club_rows = []
    for p in performances:
        club_rows.append(
            {
                "club_name": p.active_club.club.name,
                "score": p.score,
                "description": p.description,
            }
        )

    context = {
        "school": school,
        "student": student,
        "year_name": year_name,
        "semester_name": semester_name,
        "classroom": str(active_class_student.activeclass.classroom),
        "rows": rows,
        "club_rows": club_rows,
    }
    return context
