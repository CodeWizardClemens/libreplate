from django.conf import settings
from django.db import models


class DefaultMeal(models.Model):
    name = models.CharField(max_length=50)
    order = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="default_meals",
    )

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name
