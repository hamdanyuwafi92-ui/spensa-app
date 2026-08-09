from django.views.generic import DetailView
from core.models import School


class SchoolDetailView(DetailView):
    template_name = "blog/school_detail.html"
    context_object_name = "school"

    def get_object(self):
        return School.get_solo()
