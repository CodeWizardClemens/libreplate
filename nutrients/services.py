# nutrients/services.py

from .defaults import DEFAULT_NUTRIENTS
from .models import Nutrient


def sync_default_nutrients():
    for nutrient in DEFAULT_NUTRIENTS:
        Nutrient.objects.get_or_create(
            name=nutrient.name,
            defaults=nutrient.model_dump(exclude={"name"}),
        )