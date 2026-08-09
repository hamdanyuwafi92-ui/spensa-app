from django import forms
from core.models import Club


class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ("code", "name")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["code"].widget.attrs.setdefault("class", "form-control")
        self.fields["name"].widget.attrs.setdefault("class", "form-control")
