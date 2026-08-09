from django import forms
from core.models import ActiveSubject, Teacher


class ActiveSubjectForm(forms.ModelForm):
    class Meta:
        model = ActiveSubject
        fields = ("activeyear", "subject", "classroom", "teacher")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["activeyear"].widget.attrs.setdefault("class", "form-control")
        self.fields["subject"].widget.attrs.setdefault("class", "form-control")
        self.fields["classroom"].widget.attrs.setdefault("class", "form-control")
        self.fields["teacher"].widget.attrs.setdefault("class", "form-control")
        self.fields["teacher"].queryset = Teacher.objects.filter(
            job__in=["Guru", "Developer", "Administrator"]
        )
