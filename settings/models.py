# settings/models
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class UserSettings(models.Model):
    SORT_CHOICES = [
        ("name", "Name"),
        ("-created_at", "Newest"),
        ("created_at", "Oldest"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="settings")

    collapsed_sidebar = models.BooleanField(default=False)

    food_sort = models.CharField(
        max_length=50, choices=SORT_CHOICES, default="-created_at"
    )

    def __str__(self):
        return f"Settings({self.user.username})"


class DefaultMeal(models.Model):
    name = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True, null=True)

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="default_meals"
    )

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name
    

class USDAAPISettings(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="usda_api_settings",
    )
    key = models.CharField(
        max_length=64,
    )