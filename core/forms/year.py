from django import forms

from core.models import ActiveYear, Semester, Year


class YearForm(forms.ModelForm):
    class Meta:
        model = Year
        fields = ("name",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.setdefault("class", "form-control")


class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = ("name",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.setdefault("class", "form-control")


class ActiveYearForm(forms.ModelForm):
    class Meta:
        model = ActiveYear
        fields = ("year", "semester", "is_active")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["year"].widget.attrs.setdefault("class", "form-control")
        self.fields["semester"].widget.attrs.setdefault("class", "form-control")
