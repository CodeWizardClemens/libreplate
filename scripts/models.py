from django.contrib.auth.models import User
from django.db import models


class Script(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="scripts")

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    lua_version = models.CharField(max_length=32, blank=True)
    lua_code = models.TextField(blank=True, default="") 
    last_run_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
