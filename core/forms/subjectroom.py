from django import forms
from core.models import Classroom, Subject
from core.utilities.constants import LEVEL_CHOICES, SUBJECT_CHOICES


class ClassroomForm(forms.ModelForm):
    mainclassroom = forms.ChoiceField(choices=LEVEL_CHOICES)

    class Meta:
        model = Classroom
        fields = ("mainclassroom", "name")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["mainclassroom"].widget.attrs.setdefault("class", "form-control")
        self.fields["name"].widget.attrs.setdefault("class", "form-control")


class SubjectForm(forms.ModelForm):
    name = forms.ChoiceField(choices=SUBJECT_CHOICES)

    class Meta:
        model = Subject
        fields = ("code", "name")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["code"].widget.attrs.setdefault("class", "form-control")
        self.fields["name"].widget.attrs.setdefault("class", "form-control")
