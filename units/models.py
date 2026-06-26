from django.db import models
from django.contrib.auth.models import User


class Unit(models.Model):
    name = models.CharField(max_length=100, unique=True)
    name_plural = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    abbreviation = models.CharField(max_length=100, blank=True, null=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="units", null=True, blank=True
    )

    class Meta:
        verbose_name_plural = "Units"

    def __str__(self):
        return self.name
