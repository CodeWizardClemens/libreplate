from django import forms
from django.utils import timezone
from datetime import timedelta

from .models import GroceryList


class GroceryListCreateForm(forms.ModelForm):

    class Meta:

        model = GroceryList

        fields = [
            "generate_from_diary",
            "date_start",
            "date_end",
        ]

        widgets = {
            "generate_from_diary": forms.CheckboxInput(),
            "date_start": forms.DateInput(attrs={"type": "date"}),
            "date_end": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        tomorrow = timezone.localdate() + timedelta(days=1)

        self.fields["date_start"].initial = tomorrow
        self.fields["date_end"].initial = tomorrow + timedelta(days=7)
