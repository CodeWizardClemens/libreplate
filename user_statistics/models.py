from django.conf import settings
from django.db import models
from uuid import uuid4


class Graph(models.Model):

    class GraphType(models.TextChoices):
        LINE = "line", "Line Graph"
        BAR = "bar", "Bar Graph"

    class PeriodUnit(models.TextChoices):
        ALL = "all", "All Data"
        DAY = "day", "Day"
        WEEK = "week", "Week"
        MONTH = "month", "Month"
        YEAR = "year", "Year"

    class PeriodEndMode(models.TextChoices):
        LAST_DATA_POINT = "last_data_point", "Last Data Point"
        NOW = "now", "Now"
        CUSTOM = "custom", "Custom"

    class RangeType(models.TextChoices):
        FIXED = "fixed", "Fixed"
        DYNAMIC = "dynamic", "Dynamic"

    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
    )

    name = models.CharField(max_length=50)

    graph_type = models.CharField(
        max_length=20,
        choices=GraphType.choices,
    )

    period_unit = models.CharField(
        max_length=20,
        choices=PeriodUnit.choices,
        default=PeriodUnit.ALL,
    )
    period_amount = models.PositiveIntegerField(default=1)

    period_end_mode = models.CharField(
        max_length=20,
        choices=PeriodEndMode.choices,
        default=PeriodEndMode.LAST_DATA_POINT,
    )
    period_end_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Only used when period_end_mode is CUSTOM.",
    )

    range_type = models.CharField(
        max_length=20,
        choices=RangeType.choices,
        default=RangeType.DYNAMIC,
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="graphs",
    )

    def __str__(self):
        return self.name


class GraphLine(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
    )

    class MovingAverageUnit(models.TextChoices):
        DAY = "day", "Day"
        WEEK = "week", "Week"
        MONTH = "month", "Month"
        YEAR = "year", "Year"

    graph = models.ForeignKey(
        Graph,
        on_delete=models.CASCADE,
        related_name="lines",
    )

    name = models.CharField(max_length=50)

    moving_average_unit = models.CharField(
        max_length=20,
        choices=MovingAverageUnit.choices,
        null=True,
        blank=True,
    )
    moving_average_amount = models.PositiveIntegerField(
        default=1,
    )

    def clean(self):
        from django.core.exceptions import ValidationError

        has_body_metric = hasattr(self, "body_metric")
        has_nutrient = hasattr(self, "nutrient")

        if has_body_metric == has_nutrient:
            raise ValidationError(
                "A GraphLine must have exactly one of GraphLineBodyMetric or GraphLineNutrient."
            )

    def __str__(self):
        return self.name


class GraphLineBodyMetric(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
    )

    graph_line = models.OneToOneField(
        GraphLine,
        on_delete=models.CASCADE,
        related_name="body_metric",
    )

    body_metric = models.ForeignKey(
        "body_metrics.BodyMetric",
        on_delete=models.CASCADE,
    )


class GraphLineNutrient(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
    )

    graph_line = models.OneToOneField(
        GraphLine,
        on_delete=models.CASCADE,
        related_name="nutrient",
    )

    nutrient = models.ForeignKey(
        "nutrients.Nutrient",
        on_delete=models.CASCADE,
    )
