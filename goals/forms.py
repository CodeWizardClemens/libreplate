from django import forms
from .models import GoalGroup, GoalNutrient, GoalBodyMetric
from nutrients.models import Nutrient
from body_metrics.models import BodyMetric


class GoalForm(forms.ModelForm):
    class Meta:
        model = GoalGroup
        fields = [
            "name",
            "description",
            "start_date",
            "end_date",
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Summer Fitness Goals",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Describe this goal...",
                }
            ),
            "start_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "end_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
        }

    def __init__(self, *args, **kwargs):
        self.goal_group = kwargs.pop("goal_group", None)
        super().__init__(*args, **kwargs)

    def get_nutrient_values(self):
        if not self.goal_group:
            return {}

        return {
            obj.nutrient_id: obj.amount
            for obj in GoalNutrient.objects.filter(goal_group=self.goal_group)
        }

    def get_body_metric_values(self):
        if not self.goal_group:
            return {}

        return {
            obj.body_metric_id: obj.amount
            for obj in GoalBodyMetric.objects.filter(goal_group=self.goal_group)
        }

    def save_nutrients_and_metrics(self, goal_group):
        GoalNutrient.objects.filter(goal_group=goal_group).delete()
        GoalBodyMetric.objects.filter(goal_group=goal_group).delete()

        nutrients = Nutrient.objects.filter(show_in_goal_edit=True)
        body_metrics = BodyMetric.objects.filter(show_in_goal_edit=True)

        for nutrient in nutrients:
            value = self.data.get(f"nutrient_{nutrient.id}")
            if value not in (None, "", " "):
                GoalNutrient.objects.create(
                    goal_group=goal_group,
                    nutrient=nutrient,
                    amount=value,
                )

        for metric in body_metrics:
            value = self.data.get(f"metric_{metric.id}")
            if value not in (None, "", " "):
                GoalBodyMetric.objects.create(
                    goal_group=goal_group,
                    body_metric=metric,
                    amount=value,
                )