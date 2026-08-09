from django.urls import path
from core.views.brand import BrandDetailView, BrandUpdateView

app_name = "core"

urlpatterns = [
    path("brand/", BrandDetailView.as_view(), name="brand_detail"),
    path("brand/edit/", BrandUpdateView.as_view(), name="brand_edit"),
]
