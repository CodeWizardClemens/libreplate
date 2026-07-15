from django import forms

from .models import Graph, GraphLine


class GraphForm(forms.ModelForm):
    class Meta:
        model = Graph
        exclude = ["id", "user"]


class GraphLineForm(forms.ModelForm):
    class Meta:
        model = GraphLine
        exclude = ["id", "graph"]