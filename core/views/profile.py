from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView, UpdateView

from core.models import Teacher, Student
from core.forms.profile import TeacherProfileForm, StudentProfileForm
from .base import GlobalContextMixin


class ProfileBaseMixin(LoginRequiredMixin, GlobalContextMixin):
    def get_object(self):
        user = self.request.user
        if hasattr(user, "teacher"):
            return user.teacher
        elif hasattr(user, "student"):
            return user.student
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb_text"] = "Profil"
        return context


class ProfileDetailView(ProfileBaseMixin, TemplateView):
    template_name = "core/profile/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        context["profile"] = obj
        if isinstance(obj, Teacher):
            context["role"] = "teacher"
        elif isinstance(obj, Student):
            context["role"] = "student"
        else:
            context["role"] = "unknown"
        return context


class ProfileUpdateView(ProfileBaseMixin, UpdateView):
    template_name = "core/profile/profile_form.html"

    def get_form_class(self):
        obj = self.get_object()
        if isinstance(obj, Teacher):
            return TeacherProfileForm
        elif isinstance(obj, Student):
            return StudentProfileForm
        return None

    def get_object(self, queryset=None):
        return ProfileBaseMixin.get_object(self)

    def get_success_url(self):
        return "/core/profile/"

    def form_valid(self, form):
        messages.success(self.request, "Profil berhasil diperbarui.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Edit Profil"
        context["breadcrumb_text"] = "Edit Profil"
        context["role"] = (
            "teacher" if isinstance(self.get_object(), Teacher) else "student"
        )
        return context
