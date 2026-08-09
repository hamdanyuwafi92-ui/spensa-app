from django import forms


class FormControlMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(
                field.widget,
                (
                    forms.TextInput,
                    forms.Textarea,
                    forms.Select,
                    forms.EmailInput,
                    forms.URLInput,
                    forms.NumberInput,
                    forms.PasswordInput,
                    forms.ClearableFileInput,
                ),
            ):
                field.widget.attrs.setdefault("class", "form-control")
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.setdefault("class", "checkbox-group")
