# config/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin, messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.urls import include, path, re_path
from django.utils.http import url_has_allowed_host_and_scheme
from django.views import View
from django.views.decorators.http import require_POST
from django.views.static import serve


class IndexView(View):
    template_name = "index.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("core:index")
        next_url = request.GET.get("next", "")
        from core.models import Brand, School

        brand = Brand.get_solo()
        school = School.get_solo()
        return render(
            request,
            self.template_name,
            {
                "next": next_url,
                "brand": brand,
                "school": school,
            },
        )

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        next_url = request.POST.get("next", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(
                    request, f"Selamat datang, {user.get_full_name() or user.username}!"
                )
                if next_url and url_has_allowed_host_and_scheme(
                    url=next_url,
                    allowed_hosts={request.get_host()},
                    require_https=request.is_secure(),
                ):
                    return redirect(next_url)
                return redirect("core:index")
            else:
                messages.error(request, "Akun Anda telah dinonaktifkan.")
                return render(request, self.template_name, {"next": next_url})
        messages.error(request, "Username atau Password salah!")
        return render(request, self.template_name, {"next": next_url})


@require_POST
def logout_view(request):
    logout(request)
    messages.info(request, "Anda telah keluar.")
    return redirect("blog:index")


urlpatterns = [
    path("", include(("blog.urls", "blog"), namespace="blog")),
    path("core/", include(("core.urls", "core"), namespace="core")),
    path("login/", IndexView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    path("summernote/", include("django_summernote.urls")),
    path("superadmin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += [
        re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    ]
