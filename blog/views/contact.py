from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from blog.forms import MessageForm
from core.models import School


class ContactView(FormView):
    form_class = MessageForm
    template_name = "blog/kontak.html"
    success_url = reverse_lazy("blog:kontak")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["school"] = School.get_solo()
        return context

    def form_valid(self, form):
        form.save()
        messages.success(
            self.request, "Pesan berhasil terkirim! Kami akan menghubungi Anda segera."
        )
        return super().form_valid(form)
