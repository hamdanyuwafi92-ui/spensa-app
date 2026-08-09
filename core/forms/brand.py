from django import forms
from core.models import Brand


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = [
            "name",
            "description",
            "version",
            "tahun",
            "logo",
            "instagram",
            "youtube",
            "tiktok",
            "facebook",
            "developer",
        ]
        widgets = {
            "logo": forms.FileInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")
        placeholders = {
            "name": "Nama brand",
            "description": "Deskripsi singkat",
            "version": "1.0.0",
            "tahun": "2026",
            "instagram": "https://instagram.com/...",
            "youtube": "https://youtube.com/@...",
            "tiktok": "https://tiktok.com/@...",
            "facebook": "https://facebook.com/...",
            "developer": "Nama pengembang",
        }
        for field_name, placeholder in placeholders.items():
            if field_name in self.fields:
                self.fields[field_name].widget.attrs["placeholder"] = placeholder
