# settings/forms.py
from django import forms
from .models import DefaultMeal, USDAAPISettings


class DefaultMealForm(forms.ModelForm):
    class Meta:
        model = DefaultMeal
        fields = ["name", "description"]

        widgets = {
            "description": forms.Textarea(attrs={"rows": 2}),
        }


class APIConfigurationForm(forms.ModelForm):
    class Meta:
        model = USDAAPISettings
        fields = ["key"]
        labels = {
            "key": "USDA API Key",
        }
        widgets = {
            "key": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "width: 100%; max-width: 700px;",
                    "placeholder": "Enter your USDA API key",
                }
            ),
        }
