from django import forms
from .models import GoalGroup


class GoalGroupForm(forms.ModelForm):
    class Meta:
        model = GoalGroup
        fields = ["name", "note", "start_date", "end_date"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "note": forms.Textarea(
                attrs={
                    "rows": 2,
                    "cols": 40,
                }
            ),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }
