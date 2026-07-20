from .defaults import DEFAULT_NUTRIENTS
from .models import Nutrient


def sync_default_nutrients(force=False):
    for nutrient in DEFAULT_NUTRIENTS:
        data = nutrient.model_dump(exclude={"name"})

        if force:
            Nutrient.objects.update_or_create(
                name=nutrient.name,
                defaults=data,
            )
        else:
            Nutrient.objects.get_or_create(
                name=nutrient.name,
                defaults=data,
            )