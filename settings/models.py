# settings/models
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


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


class USDAAPISettings(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="usda_api_settings",
    )
    key = models.CharField(
        max_length=64,
    )
