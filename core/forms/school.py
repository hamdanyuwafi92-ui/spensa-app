from django import forms
from core.models import School


class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = [
            "name",
            "address",
            "phone",
            "email",
            "website",
            "logo",
            "npsn",
            "status",
            "jenjang",
            "akreditasi",
            "kepala_sekolah",
            "nip_kepsek",
            "fax",
            "kode_pos",
        ]
        widgets = {
            "logo": forms.FileInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")
        placeholders = {
            "name": "Nama sekolah",
            "address": "Alamat lengkap",
            "phone": "Nomor telepon",
            "email": "Email sekolah",
            "website": "https://...",
            "npsn": "8 digit",
            "kepala_sekolah": "Nama kepala sekolah",
            "nip_kepsek": "18 digit",
            "fax": "Nomor fax",
            "kode_pos": "5 digit",
        }
        for field_name, placeholder in placeholders.items():
            if field_name in self.fields:
                self.fields[field_name].widget.attrs["placeholder"] = placeholder
