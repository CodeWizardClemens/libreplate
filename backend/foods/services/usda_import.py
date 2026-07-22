from django.db import transaction

from foods.models import Food, FoodNutrient
from nutrients.models import Nutrient
from units.models import Unit

from .usda_client import USDAClient


@transaction.atomic
def import_usda_food(user, fdc_id):
    """
    Import USDA food into local DB.
    """

    if hasattr(Food, "usda_fdc_id"):
        existing = Food.objects.filter(
            user=user,
            usda_fdc_id=fdc_id,
        ).first()

        if existing:
            return existing

    client = USDAClient()
    data = client.get_food(fdc_id)

    unit = (
        Unit.objects.filter(name__iexact="g").first()
        or Unit.objects.filter(name__iexact="gram").first()
        or Unit.objects.first()
    )

    food_kwargs = {
        "user": user,
        "name": data["name"],
        "brand": data["brand"],
        "barcode": data["barcode"],
        "description": data["description"],
        "serving": data["serving"],
        "unit": unit,
    }

    if hasattr(Food, "usda_fdc_id"):
        food_kwargs["usda_fdc_id"] = data["fdc_id"]

    food = Food.objects.create(**food_kwargs)

    nutrient_lookup = {}

    for nutrient in Nutrient.objects.filter(
        usda_nutrient_number__isnull=False,
    ):
        nutrient_lookup[str(nutrient.usda_nutrient_number)] = nutrient

    for nutrient in data["nutrients"]:
        number = str(nutrient.get("number", ""))
        local_nutrient = nutrient_lookup.get(number)

        if not local_nutrient:
            continue

        FoodNutrient.objects.update_or_create(
            food=food,
            nutrient=local_nutrient,
            defaults={"amount": nutrient["value"]},
        )

    return food
