from django import forms
from django.contrib.auth import get_user_model
from core.models import Teacher

User = get_user_model()


class TeacherForm(forms.ModelForm):
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
        widget=forms.EmailInput(attrs={"placeholder": "contoh: guru@sekolah.sch.id"}),
    )

    class Meta:
        model = Teacher
        fields = [
            "nip",
            "job",
            "gender",
            "nuptk",
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
                self.fields[field_name].widget.attrs.setdefault("class", "form-control")

        for field_name in self.fields:
            self.fields[field_name].widget.attrs.setdefault("class", "form-control")

        self.fields["job"].choices = [
            # ("Developer", "Developer"),
            ("Administrator", "Administrator"),
            ("Agent", "Staff"),
            ("Guru", "Guru"),
        ]

        if self.instance and self.instance.pk and self.instance.user:
            self.fields["first_name"].initial = self.instance.user.first_name
            self.fields["last_name"].initial = self.instance.user.last_name
            self.fields["email"].initial = self.instance.user.email

    def save(self, commit=True):
        teacher = super().save(commit=False)
        user_data = {
            "first_name": self.cleaned_data["first_name"],
            "last_name": self.cleaned_data["last_name"],
            "email": self.cleaned_data.get("email"),
        }
        user = teacher.user
        if user is None:
            username = teacher.nip
            password = "guruoke123"
            user = User.objects.create_user(username=username, password=password)
            teacher.user = user
        for attr, val in user_data.items():
            setattr(user, attr, val)
        user.is_active = True
        if teacher.job == "Developer":
            user.is_staff = True
            user.is_superuser = True
        elif teacher.job in ["Administrator", "Agent", "Guru"]:
            user.is_staff = True
        else:
            user.is_staff = False
            user.is_superuser = False
        user.save()
        if commit:
            teacher.save()
        return teacher
