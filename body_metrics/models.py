from django.db import models
from django.contrib.auth.models import User


class BodyMetric(models.Model):

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    abbreviation = models.CharField(max_length=100, blank=True, null=True)

    show_in_diary_total = models.BooleanField(
        default=True, help_text="If True, this nutrient will be visible to users"
    )
    show_in_goal_edit = models.BooleanField(
        null=True,
        blank=True,
    )

    order = models.PositiveIntegerField(default=0)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="body_metric",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Nutrients"
        ordering = ["order"]

    def __str__(self):
        return self.name


class BodyMetricLog(models.Model):
    body_metric = models.ForeignKey(
        BodyMetric, on_delete=models.CASCADE, related_name="logs"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="body_metric_logs"
    )
    date = models.DateField()

    amount = models.FloatField()
    note = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ("body_metric", "user", "date")
