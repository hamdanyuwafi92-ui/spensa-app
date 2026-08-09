from django.views.generic import ListView
from core.models import Teacher, Student


class TeacherListView(ListView):
    model = Teacher
    template_name = "blog/teacher_list.html"
    context_object_name = "teachers"
    paginate_by = 12

    def get_queryset(self):
        return Teacher.objects.select_related("user").order_by("user__first_name")


class StudentListView(ListView):
    model = Student
    template_name = "blog/student_list.html"
    context_object_name = "students"
    paginate_by = 12

    def get_queryset(self):
        return Student.objects.select_related("user").order_by("user__first_name")
