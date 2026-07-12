# default_meals/signals.py

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .defaults import DEFAULT_MEALS
from .models import DefaultMeal


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_unit_scope(sender, instance, created, **kwargs):
    if not created:
        return

    DefaultMeal.objects.bulk_create(
        [
            DefaultMeal(
                user=instance,
                name=meal["name"],
                order=meal["order"],
                description=meal["description"],
            )
            for meal in DEFAULT_MEALS
        ]
    )