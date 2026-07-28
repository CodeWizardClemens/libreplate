from .defaults import DEFAULT_UNITS
from .models import Unit


def sync_default_units():
    for unit in DEFAULT_UNITS:
        Unit.objects.get_or_create(
            user=None,
            name=unit.name,
            defaults={
                "abbreviation": unit.abbreviation,
                "description": unit.description,
            },
        )
