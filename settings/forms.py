# settings/forms.py
from django import forms

from .models import USDAAPISettings

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
