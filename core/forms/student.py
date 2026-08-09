from django import forms
from django.contrib.auth import get_user_model
from core.models import Student

User = get_user_model()


class StudentForm(forms.ModelForm):
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
        widget=forms.EmailInput(attrs={"placeholder": "contoh: siswa@sekolah.sch.id"}),
    )

    class Meta:
        model = Student
        fields = [
            "nisn",
            "status",
            "nis",
            "nama_ayah",
            "nama_ibu",
            "nomor_hp_ortu",
            "gender",
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
            "nisn": "Masukkan NISN (10 digit)",
            "nis": "Masukkan NIS",
            "nama_ayah": "Nama ayah",
            "nama_ibu": "Nama ibu",
            "nomor_hp_ortu": "Contoh: 08123456789",
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
        if self.instance and self.instance.pk and self.instance.user:
            self.fields["first_name"].initial = self.instance.user.first_name
            self.fields["last_name"].initial = self.instance.user.last_name
            self.fields["email"].initial = self.instance.user.email

    def clean_nisn(self):
        nisn = self.cleaned_data.get("nisn")
        if nisn and User.objects.filter(username=nisn).exists():
            if not self.instance.pk or (self.instance.user.username != nisn):
                raise forms.ValidationError(
                    f"NISN '{nisn}' sudah terdaftar sebagai username. Silakan gunakan NISN lain."
                )
        return nisn

    def save(self, commit=True):
        student = super().save(commit=False)
        user_data = {
            "first_name": self.cleaned_data["first_name"],
            "last_name": self.cleaned_data["last_name"],
            "email": self.cleaned_data.get("email"),
        }
        user = student.user
        if user is None:
            username = student.nisn
            password = "siswaoke123"
            user = User.objects.create_user(username=username, password=password)
            student.user = user
        for attr, val in user_data.items():
            setattr(user, attr, val)
        user.is_active = True
        user.save()
        if commit:
            student.save()
        return student
