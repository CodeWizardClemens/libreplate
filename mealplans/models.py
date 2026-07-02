from django.db import models
from django.contrib.auth.models import User

class Mealplan(models.Model):

    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_used_at = models.DateTimeField(null=True, blank=True, db_index=True)

    def __str__(self):
        return self.name