from django.conf import settings
from django.db import models


class UserPreferences(models.Model):

    def theme_color_rgb(self):
        hex_color = self.theme_color.lstrip("#")
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

    theme_color = models.CharField(
        max_length=7,
        default="#0d6efd"
    )

    def __str__(self):
        return f"{self.user.username}'s preferences"