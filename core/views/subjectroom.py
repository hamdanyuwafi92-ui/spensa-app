from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView, DeleteView
from django.views.generic.edit import CreateView

from core.forms.subjectroom import ClassroomForm, SubjectForm
from core.models import Classroom, Subject
from .base import BaseAccessMixin, ModalFormMixin


class SubjectRoomContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["classrooms"] = Classroom.objects.all()
        context["subjects"] = Subject.objects.all()
        context["total_classrooms"] = Classroom.objects.count()
        context["total_subjects"] = Subject.objects.count()
        context["breadcrumb_text"] = "Kelas & Mapel"
        return context


class SubjectRoomBaseMixin(BaseAccessMixin, SubjectRoomContextMixin):
    pass


class SubjectRoomManageView(SubjectRoomBaseMixin, TemplateView):
    template_name = "core/subjectroom.html"


class ClassroomCreateView(
    SubjectRoomBaseMixin, ModalFormMixin, SuccessMessageMixin, CreateView
):
    model = Classroom
    form_class = ClassroomForm
    form_type = "classroom"
    success_url = reverse_lazy("core:subjectroom_manage")
    success_message = "Kelas berhasil ditambahkan."


class ClassroomUpdateView(
    SubjectRoomBaseMixin, ModalFormMixin, SuccessMessageMixin, UpdateView
):
    model = Classroom
    form_class = ClassroomForm
    form_type = "classroom"
    success_url = reverse_lazy("core:subjectroom_manage")
    success_message = "Kelas berhasil diperbarui."


class ClassroomDeleteView(SubjectRoomBaseMixin, SuccessMessageMixin, DeleteView):
    model = Classroom
    success_url = reverse_lazy("core:subjectroom_manage")
    success_message = "Kelas berhasil dihapus."

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class SubjectCreateView(
    SubjectRoomBaseMixin, ModalFormMixin, SuccessMessageMixin, CreateView
):
    model = Subject
    form_class = SubjectForm
    form_type = "subject"
    success_url = reverse_lazy("core:subjectroom_manage")
    success_message = "Mata pelajaran berhasil ditambahkan."


class SubjectUpdateView(
    SubjectRoomBaseMixin, ModalFormMixin, SuccessMessageMixin, UpdateView
):
    model = Subject
    form_class = SubjectForm
    form_type = "subject"
    success_url = reverse_lazy("core:subjectroom_manage")
    success_message = "Mata pelajaran berhasil diperbarui."


class SubjectDeleteView(SubjectRoomBaseMixin, SuccessMessageMixin, DeleteView):
    model = Subject
    success_url = reverse_lazy("core:subjectroom_manage")
    success_message = "Mata pelajaran berhasil dihapus."

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


# from django.contrib import messages
# from django.contrib.messages.views import SuccessMessageMixin
# from django.urls import reverse_lazy
# from django.views.generic import TemplateView, UpdateView, DeleteView
# from django.views.generic.edit import CreateView

# from core.forms.subjectroom import ClassroomForm, SubjectForm
# from core.models import Classroom, Subject
# from .base import BaseAccessMixin


# class SubjectRoomContextMixin:
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["classrooms"] = Classroom.objects.all()
#         context["subjects"] = Subject.objects.all()
#         context["total_classrooms"] = Classroom.objects.count()
#         context["total_subjects"] = Subject.objects.count()
#         context["breadcrumb_text"] = "Kelas & Mapel"
#         return context


# class SubjectRoomBaseMixin(BaseAccessMixin, SubjectRoomContextMixin):
#     pass


# class SubjectRoomManageView(SubjectRoomBaseMixin, TemplateView):
#     template_name = "core/subjectroom.html"


# class ClassroomCreateView(SubjectRoomBaseMixin, SuccessMessageMixin, CreateView):
#     model = Classroom
#     form_class = ClassroomForm
#     success_url = reverse_lazy("core:subjectroom_manage")
#     success_message = "Kelas berhasil ditambahkan."

#     def form_invalid(self, form):
#         context = self.get_context_data(form=form)
#         context["form_type"] = "classroom"
#         return self.render_to_response(context)


# class ClassroomUpdateView(SubjectRoomBaseMixin, SuccessMessageMixin, UpdateView):
#     model = Classroom
#     form_class = ClassroomForm
#     success_url = reverse_lazy("core:subjectroom_manage")
#     success_message = "Kelas berhasil diperbarui."

#     def form_invalid(self, form):
#         context = self.get_context_data(form=form)
#         context["form_type"] = "classroom"
#         return self.render_to_response(context)


# class ClassroomDeleteView(SubjectRoomBaseMixin, SuccessMessageMixin, DeleteView):
#     model = Classroom
#     success_url = reverse_lazy("core:subjectroom_manage")
#     success_message = "Kelas berhasil dihapus."

#     def delete(self, request, *args, **kwargs):
#         messages.success(self.request, self.success_message)
#         return super().delete(request, *args, **kwargs)


# class SubjectCreateView(SubjectRoomBaseMixin, SuccessMessageMixin, CreateView):
#     model = Subject
#     form_class = SubjectForm
#     success_url = reverse_lazy("core:subjectroom_manage")
#     success_message = "Mata pelajaran berhasil ditambahkan."

#     def form_invalid(self, form):
#         context = self.get_context_data(form=form)
#         context["form_type"] = "subject"
#         return self.render_to_response(context)


# class SubjectUpdateView(SubjectRoomBaseMixin, SuccessMessageMixin, UpdateView):
#     model = Subject
#     form_class = SubjectForm
#     success_url = reverse_lazy("core:subjectroom_manage")
#     success_message = "Mata pelajaran berhasil diperbarui."

#     def form_invalid(self, form):
#         context = self.get_context_data(form=form)
#         context["form_type"] = "subject"
#         return self.render_to_response(context)


# class SubjectDeleteView(SubjectRoomBaseMixin, SuccessMessageMixin, DeleteView):
#     model = Subject
#     success_url = reverse_lazy("core:subjectroom_manage")
#     success_message = "Mata pelajaran berhasil dihapus."

#     def delete(self, request, *args, **kwargs):
#         messages.success(self.request, self.success_message)
#         return super().delete(request, *args, **kwargs)


# from typing import ClassVar

# from django.contrib import messages
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.messages.views import SuccessMessageMixin
# from django.urls import reverse_lazy
# from django.views.generic import TemplateView, UpdateView, DeleteView
# from django.views.generic.edit import CreateView

# from core.models import Classroom, Subject
# from core.forms.subjectroom import ClassroomForm, SubjectForm
# from core.utilities.access import JobAccessMixin
# from .base import GlobalContextMixin


# class SubjectRoomAccessMixin(JobAccessMixin):
#     allowed_jobs: ClassVar[list[str]] = ["Developer", "Administrator"]


# class SubjectRoomContextMixin:
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["classrooms"] = Classroom.objects.all()
#         context["subjects"] = Subject.objects.all()
#         context["total_classrooms"] = Classroom.objects.count()
#         context["total_subjects"] = Subject.objects.count()
#         context["breadcrumb_text"] = "Kelas & Mapel"
#         return context


# class SubjectRoomManageView(
#     SubjectRoomAccessMixin,
#     LoginRequiredMixin,
#     GlobalContextMixin,
#     SubjectRoomContextMixin,
#     TemplateView,
# ):
#     template_name = "core/subjectroom.html"


# class ClassroomCreateView(
#     SubjectRoomAccessMixin,
#     SuccessMessageMixin,
#     SubjectRoomContextMixin,
#     GlobalContextMixin,
#     CreateView,
# ):
#     model = Classroom
#     form_class = ClassroomForm
#     template_name = "core/subjectroom.html"
#     success_url = reverse_lazy("core:subjectroom_manage")
#     success_message = "Kelas berhasil ditambahkan."

#     def form_invalid(self, form):
#         context = self.get_context_data(form=form)
#         context["form_type"] = "classroom"
#         return self.render_to_response(context)


# class ClassroomUpdateView(
#     SubjectRoomAccessMixin,
#     SuccessMessageMixin,
#     SubjectRoomContextMixin,
#     GlobalContextMixin,
#     UpdateView,
# ):
#     model = Classroom
#     form_class = ClassroomForm
#     template_name = "core/subjectroom.html"
#     success_url = reverse_lazy("core:subjectroom_manage")
#     success_message = "Kelas berhasil diperbarui."

#     def form_invalid(self, form):
#         context = self.get_context_data(form=form)
#         context["form_type"] = "classroom"
#         return self.render_to_response(context)


# class ClassroomDeleteView(
#     SubjectRoomAccessMixin,
#     SuccessMessageMixin,
#     SubjectRoomContextMixin,
#     GlobalContextMixin,
#     DeleteView,
# ):
#     model = Classroom
#     template_name = "core/subjectroom.html"
#     success_url = reverse_lazy("core:subjectroom_manage")
#     success_message = "Kelas berhasil dihapus."

#     def delete(self, request, *args, **kwargs):
#         messages.success(self.request, self.success_message)
#         return super().delete(request, *args, **kwargs)


# class SubjectCreateView(
#     SubjectRoomAccessMixin,
#     SuccessMessageMixin,
#     SubjectRoomContextMixin,
#     GlobalContextMixin,
#     CreateView,
# ):
#     model = Subject
#     form_class = SubjectForm
#     template_name = "core/subjectroom.html"
#     success_url = reverse_lazy("core:subjectroom_manage")
#     success_message = "Mata pelajaran berhasil ditambahkan."

#     def form_invalid(self, form):
#         context = self.get_context_data(form=form)
#         context["form_type"] = "subject"
#         return self.render_to_response(context)


# class SubjectUpdateView(
#     SubjectRoomAccessMixin,
#     SuccessMessageMixin,
#     SubjectRoomContextMixin,
#     GlobalContextMixin,
#     UpdateView,
# ):
#     model = Subject
#     form_class = SubjectForm
#     template_name = "core/subjectroom.html"
#     success_url = reverse_lazy("core:subjectroom_manage")
#     success_message = "Mata pelajaran berhasil diperbarui."

#     def form_invalid(self, form):
#         context = self.get_context_data(form=form)
#         context["form_type"] = "subject"
#         return self.render_to_response(context)


# class SubjectDeleteView(
#     SubjectRoomAccessMixin,
#     SuccessMessageMixin,
#     SubjectRoomContextMixin,
#     GlobalContextMixin,
#     DeleteView,
# ):
#     model = Subject
#     template_name = "core/subjectroom.html"
#     success_url = reverse_lazy("core:subjectroom_manage")
#     success_message = "Mata pelajaran berhasil dihapus."

#     def delete(self, request, *args, **kwargs):
#         messages.success(self.request, self.success_message)
#         return super().delete(request, *args, **kwargs)
