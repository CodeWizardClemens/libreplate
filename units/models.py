from uuid import uuid4

from django.conf import settings
from django.db import models
from django.db.models import Value


class UnitScope(models.Model):
    """
    Namespace for units.

    Global units use the singleton scope where user is null.
    User units use their user's scope.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="unit_scope",
        help_text=(
            "The user this scope belongs to. Leave empty for the global "
            "unit scope shared by all users."
        ),
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                # Django requires at least one expression/field to define what is
                # considered unique. Since this constraint is only concerned with the
                # existence of rows matching `user IS NULL`, we use a constant
                # expression. Every matching row has the same value (1), so the
                # database treats them as duplicates and allows only one such row.
                Value(1),
                condition=models.Q(user__isnull=True),
                name="only_one_global_unit_scope",
            ),
        ]

    def __str__(self):
        return "global scope" if self.user is None else f"{self.user}'s scope"


class Unit(models.Model):
    """
    Represents a unit of measurement within a specific unit scope.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
    )

    scope = models.ForeignKey(
        UnitScope,
        on_delete=models.CASCADE,
        related_name="units",
    )

    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    abbreviation = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["scope", "name"],
                name="unique_unit_name_per_scope",
            )
        ]

    def __str__(self):
        return self.name
