from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView, DeleteView
from django.views.generic.edit import CreateView

from core.forms.club import ClubForm
from core.models import Club
from .base import BaseAccessMixin, ModalFormMixin


class ClubContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["clubs"] = Club.objects.all()
        context["total_clubs"] = Club.objects.count()
        context["breadcrumb_text"] = "Ekstrakurikuler"
        return context


class ClubBaseMixin(BaseAccessMixin, ClubContextMixin):
    pass


class ClubManageView(ClubBaseMixin, TemplateView):
    template_name = "core/club.html"


class ClubCreateView(ClubBaseMixin, ModalFormMixin, SuccessMessageMixin, CreateView):
    model = Club
    form_class = ClubForm
    form_type = "club"
    success_url = reverse_lazy("core:club_manage")
    success_message = "Ekstrakurikuler berhasil ditambahkan."


class ClubUpdateView(ClubBaseMixin, ModalFormMixin, SuccessMessageMixin, UpdateView):
    model = Club
    form_class = ClubForm
    form_type = "club"
    success_url = reverse_lazy("core:club_manage")
    success_message = "Ekstrakurikuler berhasil diperbarui."


class ClubDeleteView(ClubBaseMixin, SuccessMessageMixin, DeleteView):
    model = Club
    success_url = reverse_lazy("core:club_manage")
    success_message = "Ekstrakurikuler berhasil dihapus."

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


# from django.contrib import messages
# from django.contrib.messages.views import SuccessMessageMixin
# from django.urls import reverse_lazy
# from django.views.generic import TemplateView, UpdateView, DeleteView
# from django.views.generic.edit import CreateView

# from core.forms.club import ClubForm
# from core.models import Club
# from .base import BaseAccessMixin


# class ClubContextMixin:
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["clubs"] = Club.objects.all()
#         context["total_clubs"] = Club.objects.count()
#         context["breadcrumb_text"] = "Ekstrakurikuler"
#         return context


# class ClubBaseMixin(BaseAccessMixin, ClubContextMixin):
#     pass


# class ClubManageView(ClubBaseMixin, TemplateView):
#     template_name = "core/club.html"


# class ClubCreateView(ClubBaseMixin, SuccessMessageMixin, CreateView):
#     model = Club
#     form_class = ClubForm
#     success_url = reverse_lazy("core:club_manage")
#     success_message = "Ekstrakurikuler berhasil ditambahkan."

#     def form_invalid(self, form):
#         context = self.get_context_data(form=form)
#         context["form_type"] = "club"
#         return self.render_to_response(context)


# class ClubUpdateView(ClubBaseMixin, SuccessMessageMixin, UpdateView):
#     model = Club
#     form_class = ClubForm
#     success_url = reverse_lazy("core:club_manage")
#     success_message = "Ekstrakurikuler berhasil diperbarui."

#     def form_invalid(self, form):
#         context = self.get_context_data(form=form)
#         context["form_type"] = "club"
#         return self.render_to_response(context)


# class ClubDeleteView(ClubBaseMixin, SuccessMessageMixin, DeleteView):
#     model = Club
#     success_url = reverse_lazy("core:club_manage")
#     success_message = "Ekstrakurikuler berhasil dihapus."

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

# from core.models import Club
# from core.forms.club import ClubForm
# from core.utilities.access import JobAccessMixin
# from .base import GlobalContextMixin


# class ClubAccessMixin(JobAccessMixin):
#     allowed_jobs: ClassVar[list[str]] = ["Developer", "Administrator"]


# class ClubContextMixin:
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["clubs"] = Club.objects.all()
#         context["total_clubs"] = Club.objects.count()
#         context["breadcrumb_text"] = "Ekstrakurikuler"
#         return context


# class ClubManageView(
#     ClubAccessMixin,
#     LoginRequiredMixin,
#     GlobalContextMixin,
#     ClubContextMixin,
#     TemplateView,
# ):
#     template_name = "core/club.html"


# class ClubCreateView(
#     ClubAccessMixin,
#     SuccessMessageMixin,
#     ClubContextMixin,
#     GlobalContextMixin,
#     CreateView,
# ):
#     model = Club
#     form_class = ClubForm
#     template_name = "core/club.html"
#     success_url = reverse_lazy("core:club_manage")
#     success_message = "Ekstrakurikuler berhasil ditambahkan."

#     def form_invalid(self, form):
#         context = self.get_context_data(form=form)
#         context["form_type"] = "club"
#         return self.render_to_response(context)


# class ClubUpdateView(
#     ClubAccessMixin,
#     SuccessMessageMixin,
#     ClubContextMixin,
#     GlobalContextMixin,
#     UpdateView,
# ):
#     model = Club
#     form_class = ClubForm
#     template_name = "core/club.html"
#     success_url = reverse_lazy("core:club_manage")
#     success_message = "Ekstrakurikuler berhasil diperbarui."

#     def form_invalid(self, form):
#         context = self.get_context_data(form=form)
#         context["form_type"] = "club"
#         return self.render_to_response(context)


# class ClubDeleteView(
#     ClubAccessMixin,
#     SuccessMessageMixin,
#     ClubContextMixin,
#     GlobalContextMixin,
#     DeleteView,
# ):
#     model = Club
#     template_name = "core/club.html"
#     success_url = reverse_lazy("core:club_manage")
#     success_message = "Ekstrakurikuler berhasil dihapus."

#     def delete(self, request, *args, **kwargs):
#         messages.success(self.request, self.success_message)
#         return super().delete(request, *args, **kwargs)
