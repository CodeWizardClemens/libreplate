# body_metrics/forms.py
from django import forms

from .models import BodyMetric


class BodyMetricForm(forms.ModelForm):
    class Meta:
        model = BodyMetric
        fields = ["name", "abbreviation", "description", "show_in_diary_total"]

        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }
