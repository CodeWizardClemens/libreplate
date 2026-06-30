from django import forms

from .models import Automation


class AutomationForm(forms.ModelForm):
    class Meta:
        model = Automation
        fields = [
            "name",
            "description",
            "lua_code",
        ]

        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
            "lua_code": forms.Textarea(
                attrs={
                    "rows": 30,
                    "spellcheck": "false",
                    "class": "code-editor",
                    "style": "width:100%;font-family:monospace;",
                }
            ),
        }
