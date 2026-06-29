# nutrients/models
from django.contrib.auth.models import User
from django.db import models


class Nutrient(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    abbreviation = models.CharField(max_length=100, blank=True, null=True)

    show_in_diary_total = models.BooleanField(
        null=True,
        blank=True,
        help_text="Show this nutrient in diary totals.",
    )

    show_in_diary_meal = models.BooleanField(
        null=True,
        blank=True,
        help_text="Show this nutrient in individual diary meals.",
    )

    show_in_food_edit = models.BooleanField(
        null=True,
        blank=True,
        help_text="Show this nutrient when editing a food.",
    )

    show_in_recipe = models.BooleanField(
        null=True,
        blank=True,
        help_text="Show this nutrient in recipes.",
    )

    show_in_foods = models.BooleanField(
        null=True,
        blank=True,
        help_text="Show this nutrient in food detail/list pages.",
    )

    show_in_goal_edit = models.BooleanField(
        null=True,
        blank=True,
    )
    usda_nutrient_number = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        unique=True,
        help_text="USDA nutrient number (e.g. 1003 for Protein).",
    )

    order = models.PositiveIntegerField(default=0)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="nutrients",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Nutrients"
        ordering = ["order"]

    def __str__(self):
        return self.name
