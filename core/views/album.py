from typing import ClassVar

from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from django.views.generic.edit import DeletionMixin

from core.models import Album, Photo
from core.utilities.validators import validate_logo

from .base import GlobalContextMixin


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ("title", "thumbnail", "caption")
        widgets: ClassVar[dict] = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(
                field.widget,
                (
                    forms.TextInput,
                    forms.Textarea,
                    forms.Select,
                    forms.EmailInput,
                    forms.URLInput,
                    forms.NumberInput,
                    forms.PasswordInput,
                    forms.ClearableFileInput,
                ),
            ):
                field.widget.attrs.setdefault("class", "form-control")
        self.fields["thumbnail"].validators.append(validate_logo)


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ("image", "caption")
        widgets: ClassVar[dict] = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(
                field.widget, (forms.TextInput, forms.URLInput, forms.Textarea)
            ):
                field.widget.attrs.setdefault("class", "form-control")


class AlbumContextMixin(LoginRequiredMixin, GlobalContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_albums"] = Album.objects.count()
        context["breadcrumb_text"] = "Album"
        return context


class AlbumListView(AlbumContextMixin, ListView):
    template_name = "core/album.html"
    context_object_name = "albums"
    paginate_by = 10

    def get_queryset(self):
        return (
            Album.objects.select_related("created_by")
            .annotate(num_photos=Count("photo"))
            .order_by("-created_at")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_mode"] = "list"
        return context


class AlbumCreateView(AlbumContextMixin, SuccessMessageMixin, CreateView):
    model = Album
    form_class = AlbumForm
    template_name = "core/album.html"
    success_url = reverse_lazy("core:album_list")
    success_message = "Album berhasil dibuat."

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_mode"] = "create"
        context["form_title"] = "Tambah Album Baru"
        return context


class AlbumUpdateView(AlbumContextMixin, SuccessMessageMixin, UpdateView):
    model = Album
    form_class = AlbumForm
    template_name = "core/album.html"
    success_url = reverse_lazy("core:album_list")
    success_message = "Album berhasil diperbarui."

    def get_queryset(self):
        return Album.objects.filter(created_by=self.request.user)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.created_by != self.request.user:
            raise Http404("Album tidak ditemukan.")
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_mode"] = "update"
        context["form_title"] = "Edit Album"
        return context


class AlbumDeleteView(AlbumContextMixin, SuccessMessageMixin, DeleteView):
    model = Album
    template_name = "core/album.html"
    success_url = reverse_lazy("core:album_list")
    success_message = "Album berhasil dihapus."

    def get_queryset(self):
        return Album.objects.filter(created_by=self.request.user)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.created_by != self.request.user:
            raise Http404("Album tidak ditemukan.")
        return obj

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class AlbumManageView(LoginRequiredMixin, GlobalContextMixin, DetailView):
    model = Album
    template_name = "core/album/manage.html"
    context_object_name = "album"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.created_by != self.request.user:
            raise Http404("Album tidak ditemukan.")
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["photos"] = self.object.photo_set.order_by("-created_at")
        context["form"] = PhotoForm(initial={"album": self.object})
        context["breadcrumb_text"] = f"Kelola Album: {self.object.title}"
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = PhotoForm(request.POST)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.album = self.object
            photo.created_by = request.user
            photo.save()
            messages.success(request, "Foto berhasil ditambahkan.")
            return redirect("core:album_manage", slug=self.object.slug)
        # jika form tidak valid, render ulang halaman dengan form error
        context = self.get_context_data(object=self.object)
        context["form"] = form
        return self.render_to_response(context)


class PhotoDeleteView(
    LoginRequiredMixin, DeletionMixin, SuccessMessageMixin, DetailView
):
    model = Photo
    success_message = "Foto berhasil dihapus."

    def get_success_url(self):
        return reverse("core:album_manage", kwargs={"slug": self.object.album.slug})

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.album.created_by != self.request.user:
            raise Http404("Foto tidak ditemukan.")
        return obj

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)
