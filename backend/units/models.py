from django.conf import settings
from django.db import models
from django.db.models import Q


class Unit(models.Model):
    """
    Represents a unit of measurement.

    A unit can either be:
    - global (user is NULL)
    - owned by a specific user
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="units",
        help_text="Leave empty for a global unit.",
    )

    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    abbreviation = models.CharField(max_length=15, blank=True)

    # TODO "visable", is not a good name for it. It should be more descriptive.
    # These flags mean that it shows in a dropdown menu for a user when they can
    # pick a unit.
    visible_in_nutrients = models.BooleanField(default=False)
    visible_in_body_metrics = models.BooleanField(default=False)
    visible_in_foods = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["name"],
                condition=Q(user__isnull=True),
                name="unique_global_unit_name",
            ),
            models.UniqueConstraint(
                fields=["user", "name"],
                condition=Q(user__isnull=False),
                name="unique_user_unit_name",
            ),
        ]

    def __str__(self):
        return self.name
