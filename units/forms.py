# units/forms.py
from django import forms
from .models import Unit


class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ["name", "name_plural", "abbreviation", "description"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }
