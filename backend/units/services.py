# units/services.py

from .defaults import DEFAULT_UNITS
from .models import Unit, UnitScope


def sync_default_units():
    global_scope, _ = UnitScope.objects.get_or_create(user=None)

    for unit in DEFAULT_UNITS:
        Unit.objects.get_or_create(
            scope=global_scope,
            name=unit.name,
            defaults=unit.model_dump(exclude={"name"}),
        )
