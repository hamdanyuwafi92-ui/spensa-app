from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from core.models import Teacher, Student

User = get_user_model()


class BaseProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=150,
        required=True,
        label="Nama Depan",
        widget=forms.TextInput(attrs={"placeholder": "Masukkan nama depan"}),
    )
    last_name = forms.CharField(
        max_length=150,
        required=True,
        label="Nama Belakang",
        widget=forms.TextInput(attrs={"placeholder": "Masukkan nama belakang"}),
    )
    email = forms.EmailField(
        required=False,
        label="Email",
        widget=forms.EmailInput(attrs={"placeholder": "contoh: nama@sekolah.sch.id"}),
    )
    password1 = forms.CharField(
        label="Password Baru",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Kosongkan jika tidak ingin mengubah"}
        ),
        required=False,
    )
    password2 = forms.CharField(
        label="Konfirmasi Password Baru",
        strip=False,
        widget=forms.PasswordInput(attrs={"placeholder": "Ulangi password baru"}),
        required=False,
    )

    class Meta:
        abstract = True

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")
        if p1 or p2:
            if p1 != p2:
                raise forms.ValidationError("Password baru tidak cocok.")
            validate_password(p1)
        return cleaned_data

    def save(self, commit=True):
        obj = super().save(commit=False)
        user = obj.user
        if user:
            user.first_name = self.cleaned_data["first_name"]
            user.last_name = self.cleaned_data["last_name"]
            user.email = self.cleaned_data.get("email", "")
            p1 = self.cleaned_data.get("password1")
            if p1:
                user.set_password(p1)
            user.save()
        if commit:
            obj.save()
        return obj


class TeacherProfileForm(BaseProfileForm):
    class Meta:
        model = Teacher
        fields = [
            "nip",
            "nuptk",
            "gender",
            "gelar_depan",
            "gelar_belakang",
            "tempat_lahir",
            "tanggal_lahir",
            "alamat",
            "nomor_hp",
            "photo",
        ]
        widgets = {
            "tanggal_lahir": forms.DateInput(attrs={"type": "date"}),
            "photo": forms.FileInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")
        placeholders = {
            "nip": "Masukkan NIP (18 digit)",
            "nuptk": "Masukkan NUPTK (16 digit)",
            "gelar_depan": "Contoh: Drs.",
            "gelar_belakang": "Contoh: S.Pd., M.M.",
            "tempat_lahir": "Kota kelahiran",
            "alamat": "Alamat lengkap",
            "nomor_hp": "Contoh: 08123456789",
        }
        for field_name, placeholder in placeholders.items():
            if field_name in self.fields:
                self.fields[field_name].widget.attrs["placeholder"] = placeholder
        if self.instance and self.instance.pk and self.instance.user:
            self.fields["first_name"].initial = self.instance.user.first_name
            self.fields["last_name"].initial = self.instance.user.last_name
            self.fields["email"].initial = self.instance.user.email


class StudentProfileForm(BaseProfileForm):
    class Meta:
        model = Student
        fields = [
            "nisn",
            "nis",
            "gender",
            "tempat_lahir",
            "tanggal_lahir",
            "alamat",
            "nama_ayah",
            "nama_ibu",
            "nomor_hp_ortu",
            "nomor_hp",
            "photo",
        ]
        widgets = {
            "tanggal_lahir": forms.DateInput(attrs={"type": "date"}),
            "photo": forms.FileInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")
        placeholders = {
            "nisn": "Masukkan NISN (10 digit)",
            "nis": "Masukkan NIS",
            "tempat_lahir": "Kota kelahiran",
            "alamat": "Alamat lengkap",
            "nama_ayah": "Nama ayah",
            "nama_ibu": "Nama ibu",
            "nomor_hp_ortu": "Contoh: 08123456789",
            "nomor_hp": "Contoh: 08123456789",
        }
        for field_name, placeholder in placeholders.items():
            if field_name in self.fields:
                self.fields[field_name].widget.attrs["placeholder"] = placeholder
        if self.instance and self.instance.pk and self.instance.user:
            self.fields["first_name"].initial = self.instance.user.first_name
            self.fields["last_name"].initial = self.instance.user.last_name
            self.fields["email"].initial = self.instance.user.email
