from django.conf import settings
from django.db import models


class GoalGroup(models.Model):
    name = models.CharField(max_length=255)
    note = models.TextField(blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="goal_groups",
    )
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name


class GoalNutrient(models.Model):
    nutrient = models.ForeignKey("nutrients.Nutrient", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    goal_group = models.ForeignKey(
        GoalGroup,
        on_delete=models.CASCADE,
        related_name="nutrient_goals",
    )

    def __str__(self):
        return f"{self.nutrient.name} - {self.amount}"


class GoalBodyMetric(models.Model):
    body_metric = models.ForeignKey(
        "body_metrics.BodyMetric",
        on_delete=models.CASCADE,
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    goal_group = models.ForeignKey(
        GoalGroup,
        on_delete=models.CASCADE,
        related_name="body_measurement_goals",
    )

    def __str__(self):
        return f"{self.body_metric.name} - {self.amount}"
