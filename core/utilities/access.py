from typing import ClassVar

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import TemplateView


def get_user_jobs(user):
    if not user.is_authenticated:
        return []
    if user.is_superuser:
        return ["Developer"]
    jobs = []
    if hasattr(user, "teacher") and user.teacher:
        jobs.append(user.teacher.job)
    if hasattr(user, "student") and user.student:
        jobs.append("Siswa")
    return jobs


class JobAccessMixin(LoginRequiredMixin):
    allowed_jobs: ClassVar[list[str]] = []

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        user_jobs = get_user_jobs(request.user)
        if not any(job in self.allowed_jobs for job in user_jobs):
            raise PermissionDenied("Anda tidak memiliki akses ke halaman ini.")
        return super().dispatch(request, *args, **kwargs)


class DeveloperViews(JobAccessMixin, TemplateView):
    allowed_jobs: ClassVar[list[str]] = ["Developer"]


class AdministratorViews(JobAccessMixin, TemplateView):
    allowed_jobs: ClassVar[list[str]] = ["Administrator", "Developer"]


class StaffViews(JobAccessMixin, TemplateView):
    allowed_jobs: ClassVar[list[str]] = ["Agent", "Developer", "Administrator"]


class GuruViews(JobAccessMixin, TemplateView):
    allowed_jobs: ClassVar[list[str]] = ["Guru", "Developer", "Administrator"]


class SiswaViews(JobAccessMixin, TemplateView):
    allowed_jobs: ClassVar[list[str]] = ["Siswa"]


class DevAdminAccessMixin(JobAccessMixin):
    allowed_jobs: ClassVar[list[str]] = ["Developer", "Administrator"]


# from typing import ClassVar

# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.core.exceptions import PermissionDenied
# from django.views.generic import TemplateView


# def get_user_jobs(user):
#     if not user.is_authenticated:
#         return []
#     if user.is_superuser:
#         return ["Developer"]
#     jobs = []
#     # Staff users (named Agent in frontend) may not have a Teacher profile
#     if user.is_staff:
#         jobs.append("Agent")
#     if hasattr(user, "teacher") and user.teacher:
#         jobs.append(user.teacher.job)
#     if hasattr(user, "student") and user.student:
#         jobs.append("Siswa")
#     return jobs


# class JobAccessMixin(LoginRequiredMixin):
#     allowed_jobs: ClassVar[list[str]] = []

#     def dispatch(self, request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             return self.handle_no_permission()
#         user_jobs = get_user_jobs(request.user)
#         if not any(job in self.allowed_jobs for job in user_jobs):
#             raise PermissionDenied("Anda tidak memiliki akses ke halaman ini.")
#         return super().dispatch(request, *args, **kwargs)


# class DeveloperViews(JobAccessMixin, TemplateView):
#     allowed_jobs: ClassVar[list[str]] = ["Developer"]


# class AdministratorViews(JobAccessMixin, TemplateView):
#     allowed_jobs: ClassVar[list[str]] = ["Administrator", "Developer"]


# class StaffViews(JobAccessMixin, TemplateView):
#     allowed_jobs: ClassVar[list[str]] = ["Staff", "Developer", "Administrator"]


# class GuruViews(JobAccessMixin, TemplateView):
#     allowed_jobs: ClassVar[list[str]] = ["Guru", "Developer", "Administrator"]


# class SiswaViews(JobAccessMixin, TemplateView):
#     allowed_jobs: ClassVar[list[str]] = ["Siswa"]


# class DevAdminAccessMixin(JobAccessMixin):
#     allowed_jobs: ClassVar[list[str]] = ["Developer", "Administrator"]
