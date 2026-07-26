# default_meals/signals.py

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .defaults import get_default_meals
from .models import DefaultMeal


@receiver(post_save, sender=User)
def create_default_meals(sender, instance, created, **kwargs):
    if not created:
        return

    DefaultMeal.objects.bulk_create(get_default_meals(user=instance))
