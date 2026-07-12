from uuid import uuid4

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Value


class UnitScope(models.Model):
    """
    Namespace for units.

    Global units use the singleton scope where user is null.
    User units use their user's scope.
    """

    # TODO There should be some logic for when a global unit is created, and a user
    # has already defined one. This will have to be handled properly whenupdating
    # the server via proper migrations.

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

    Rules:
    - Unit names must be unique within a scope.
    - If a unit exists in the global scope, users cannot create a unit with
      the same name in their private scope.
    - Different users may share the same private unit name, provided it does
      not exist globally.
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
            ),
        ]

    # TODO Possible race conditions introduced with this clean and save function.
    # Replace with a constraint, or add a database lock.
    def clean(self):
        super().clean()

        # Scope hasn't been assigned yet (e.g. during form validation).
        if self.scope_id is None:
            return

        # Global units have no restriction.
        if self.scope.user is None:
            return

        if Unit.objects.filter(
            scope__user__isnull=True,
            name=self.name,
        ).exclude(pk=self.pk).exists():
            raise ValidationError(
                {
                    "name": (
                        "A global unit with this name already exists. "
                        "User-defined units cannot override global units."
                    )
                }
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class HiddenUnit(models.Model):
    """
    Stores which units a user has chosen to hide from unit selection interface.

    Each record represents a single (user, unit) combination. If no
    HiddenUnit exists for a pair, the unit is considered visible.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="hidden_units",
    )

    unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
        related_name="hidden_by_users",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "unit"],
                name="unique_hidden_unit_per_user",
            ),
        ]
