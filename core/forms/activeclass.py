from django import forms
from core.models import ActiveClass, ActiveClassStudent, Student, Teacher


class ActiveClassForm(forms.ModelForm):
    class Meta:
        model = ActiveClass
        fields = ("activeyear", "classroom", "capacity", "teacher")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["activeyear"].widget.attrs.setdefault("class", "form-control")
        self.fields["classroom"].widget.attrs.setdefault("class", "form-control")
        self.fields["capacity"].widget.attrs.setdefault("class", "form-control")
        self.fields["teacher"].widget.attrs.setdefault("class", "form-control")
        self.fields["teacher"].queryset = Teacher.objects.filter(
            job__in=["Guru", "Developer", "Administrator", "Agent"]
        )


class AddStudentForm(forms.Form):
    student = forms.ModelChoiceField(
        queryset=Student.objects.all(),
        label="Pilih Siswa",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
