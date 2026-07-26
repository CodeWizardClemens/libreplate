# default_meals/signals.py

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import DefaultMeal
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .defaults import get_default_meals
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


@receiver(post_save, sender=User)
def create_default_meals(sender, instance, created, **kwargs):
    if not created:
        return

    DefaultMeal.objects.bulk_create(
        get_default_meals(user=instance)
    )
