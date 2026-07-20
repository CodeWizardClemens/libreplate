from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q


class BodyMetric(models.Model):

    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    show_in_diary_total = models.BooleanField(
        default=True,
    )
    show_in_goal_edit = models.BooleanField(
        default=True,
    )
    is_single_entry = models.BooleanField(
        default=False,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="body_metric",
        null=True,
        help_text="If True, this nutrient will be visible to users",
    )

    class Meta:
        verbose_name = "Nutrients"
        constraints = [
            # Global metrics
            models.UniqueConstraint(
                fields=["name"],
                condition=Q(user__isnull=True),
                name="unique_global_body_metric_name",
            ),
            # Per-user metrics
            models.UniqueConstraint(
                fields=["user", "name"],
                condition=Q(user__isnull=False),
                name="unique_user_body_metric_name",
            ),
        ]

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
