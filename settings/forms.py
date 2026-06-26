# settings/forms.py
from django import forms
from .models import DefaultMeal


class DefaultMealForm(forms.ModelForm):
    class Meta:
        model = DefaultMeal
        fields = ["name", "description"]

        widgets = {
            "description": forms.Textarea(attrs={"rows": 2}),
        }
