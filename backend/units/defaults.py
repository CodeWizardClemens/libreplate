from .models import Unit

DEFAULT_UNITS = [
    Unit(
        name="Gram",
        abbreviation="g",
        description="SI unit of mass.",
    ),
    Unit(
        name="Milliliter",
        abbreviation="ml",
        description="SI unit of volume.",
    ),
    Unit(
        name="Piece",
        abbreviation="",
        description="A piece of something.",
    ),
    Unit(
        name="Scoop",
        abbreviation="",
        description="A scoop of something.",
    ),
]
