from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from core.models import ActiveYear, Brand, School
from core.utilities.access import DevAdminAccessMixin as IsDevAdminPermission


class GlobalContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        brand = Brand.get_solo()
        school = School.get_solo()
        active_year = ActiveYear.get_active()
        context.update(
            {
                "brand": brand,
                "school": school,
                "active_year": active_year,
                "breadcrumb_text": "",
            }
        )
        return context


class BaseView(LoginRequiredMixin, GlobalContextMixin, TemplateView):
    pass


class BaseAccessMixin(IsDevAdminPermission, GlobalContextMixin):
    pass


class BaseAuthMixin(LoginRequiredMixin, GlobalContextMixin):
    pass


class ModalFormMixin:
    form_type = None

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        context["form_type"] = self.form_type
        return self.render_to_response(context)


# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.views.generic import TemplateView

# from core.models import ActiveYear, Brand, School
# from core.utilities.access import DevAdminAccessMixin as IsDevAdminPermission


# class GlobalContextMixin:
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         brand = Brand.get_solo()
#         school = School.get_solo()
#         active_year = ActiveYear.get_active()
#         context.update(
#             {
#                 "brand": brand,
#                 "school": school,
#                 "active_year": active_year,
#                 "breadcrumb_text": "",
#             }
#         )
#         return context


# class BaseView(LoginRequiredMixin, GlobalContextMixin, TemplateView):
#     pass


# class BaseAccessMixin(IsDevAdminPermission, GlobalContextMixin):
#     pass


# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.views.generic import TemplateView

# from core.models import ActiveYear, Brand, School


# class GlobalContextMixin:
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         brand = Brand.get_solo()
#         school = School.get_solo()
#         active_year = ActiveYear.get_active()
#         context.update(
#             {
#                 "brand": brand,
#                 "school": school,
#                 "active_year": active_year,
#                 "breadcrumb_text": "",
#             }
#         )
#         return context


# class BaseView(LoginRequiredMixin, GlobalContextMixin, TemplateView):
#     pass
