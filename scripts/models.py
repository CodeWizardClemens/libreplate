from django.contrib.auth.models import User
from django.db import models


class Script(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="scripts")

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ScriptStep(models.Model):
    script = models.ForeignKey(Script, on_delete=models.CASCADE, related_name="steps")

    order = models.PositiveIntegerField(default=0)

    function_key = models.CharField(max_length=100)

    config = models.JSONField(default=dict)

    class Meta:
        ordering = ["order"]
