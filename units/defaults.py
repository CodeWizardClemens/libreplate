from pydantic import BaseModel


class UnitSchema(BaseModel):
    name: str
    abbreviation: str = ""
    description: str = ""


DEFAULT_UNITS = [
    UnitSchema(
        name="Gram",
        abbreviation="g",
        description="SI unit of mass.",
    ),
    UnitSchema(
        name="Milliliter",
        abbreviation="ml",
        description="SI unit of volume.",
    ),
    UnitSchema(
        name="Piece",
        abbreviation="",
        description="A piece of something.",
    ),
    UnitSchema(
        name="Scoop",
        abbreviation="",
        description="A scoop of something.",
    ),
]