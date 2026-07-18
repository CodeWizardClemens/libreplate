from django.conf import settings
from django.db import models


class UserPreferences(models.Model):
    SORT_CHOICES = [
        ("name", "Name"),
        ("-created_at", "Newest"),
        ("created_at", "Oldest"),
    ]
    def theme_color_rgb(self):
        hex_color = self.theme_color.lstrip("#")

        if len(hex_color) != 6:
            return "13,110,253"

        return ",".join(
            str(int(hex_color[i:i+2], 16))
            for i in (0, 2, 4)
        )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="preferences"
    )

    dark_mode = models.BooleanField(default=False)

    food_sort_mode = models.CharField(
        max_length=50, choices=SORT_CHOICES, default="-created_at"
    )

    theme_color = models.CharField(
        max_length=7,
        default="#0d6efd"
    )

    def __str__(self):
        return f"{self.user.username}'s preferences"