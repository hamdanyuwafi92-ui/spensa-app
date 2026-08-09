from django import forms
from core.models import ActiveClub, Student, Teacher


class ActiveClubForm(forms.ModelForm):
    class Meta:
        model = ActiveClub
        fields = ("activeyear", "club", "teacher")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["activeyear"].widget.attrs.setdefault("class", "form-control")
        self.fields["club"].widget.attrs.setdefault("class", "form-control")
        self.fields["teacher"].widget.attrs.setdefault("class", "form-control")
        self.fields["teacher"].queryset = Teacher.objects.filter(
            job__in=["Guru", "Developer", "Administrator", "Agent"]
        )


class AddStudentToClubForm(forms.Form):
    student = forms.ModelChoiceField(
        queryset=Student.objects.all(),
        label="Pilih Siswa",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
