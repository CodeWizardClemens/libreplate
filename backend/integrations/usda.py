from __future__ import annotations

from decimal import Decimal
from functools import lru_cache
from typing import Any

import requests
from django.contrib.auth.models import User
from django.db import transaction

from foods.models import Food, FoodNutrient
from integrations.models import USDAAPISettings
from nutrients.models import Nutrient
from units.models import Unit, UnitScope

USDA_API_BASE_URL = "https://api.nal.usda.gov/fdc/v1"

MAX_PAGE_SIZE = 50
MIN_PAGE_SIZE = 1

MAX_PAGE_NUMBER = 1000
MIN_PAGE_NUMBER = 1


class USDAError(Exception):
    """Raised when the USDA API cannot be queried successfully."""


def _validate_pagination(
    page_size: int,
    page_number: int,
) -> None:
    if page_size < MIN_PAGE_SIZE:
        raise USDAError("page_size must be greater than zero.")

    if page_size > MAX_PAGE_SIZE:
        raise USDAError(f"page_size cannot exceed {MAX_PAGE_SIZE}.")

    if page_number < MIN_PAGE_NUMBER:
        raise USDAError("page_number must start at 1.")

    if page_number > MAX_PAGE_NUMBER:
        raise USDAError(f"page_number cannot exceed {MAX_PAGE_NUMBER}.")


def _normalize_food_name(name: str) -> str:
    """
    Fix USDA names that are entirely uppercase.

    A lot of USDA food names are stored like this and look ugly.
    """
    if name.isupper():
        return name.capitalize()

    return name


def _get_api_key() -> str:
    try:
        return USDAAPISettings.objects.get().key
    except USDAAPISettings.DoesNotExist as exc:
        raise USDAError("USDA API key is not configured.") from exc


def _request(
    endpoint: str,
    *,
    params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    api_key = _get_api_key()

    params = {
        **(params or {}),
        "api_key": api_key,
    }

    response = requests.get(
        f"{USDA_API_BASE_URL}/{endpoint}",
        params=params,
        timeout=10,
    )

    if response.status_code == 404:
        raise USDAError("Food not found.")

    if not response.ok:
        raise USDAError(
            f"USDA API error: {response.status_code} {response.text}"
        )

    return response.json()


@lru_cache(maxsize=128)
def _search_foods(
    term: str,
    *,
    page_size: int = 25,
    page_number: int = 1,
) -> dict[str, Any]:
    """
    Fetch raw food records from USDA FoodData Central.

    The USDA API returns JSON objects. These objects are converted into
    Django Food model instances by `search()`.
    """

    return _request(
        "foods/search",
        params={
            "generalSearchInput": term,
            "pageSize": page_size,
            "pageNumber": page_number,
        },
    )


@lru_cache(maxsize=128)
def _get_food(fdc_id: int) -> dict[str, Any]:
    """
    Fetch a single raw USDA food record by FDC ID.
    """
    return _request(f"food/{fdc_id}")


def _get_global_unit(name: str) -> Unit | None:
    """
    USDA units are mapped only against global units.
    """
    try:
        scope = UnitScope.objects.get(user=None)
    except UnitScope.DoesNotExist:
        return None

    normalized = name.lower()

    mapping = {
        "g": "Gram",
        "gram": "Gram",
        "grams": "Gram",
        "ml": "Milliliter",
        "milliliter": "Milliliter",
        "milliliters": "Milliliter",
    }

    unit_name = mapping.get(normalized)

    if not unit_name:
        return None

    return Unit.objects.filter(
        scope=scope,
        name=unit_name,
    ).first()


def _extract_brand(food: dict[str, Any]) -> str | None:
    return food.get("brandOwner") or food.get("brandName") or None


def _create_unsaved_food(
    food_data: dict[str, Any],
    *,
    user: User,
) -> Food:
    """
    Convert a USDA food JSON object into an unsaved Django Food object.

    The returned Food instance is not stored in the database until saved.
    """

    serving = Decimal("100")

    unit = _get_global_unit("g")

    name = food_data.get(
        "description",
        "Unknown food",
    )

    return Food(
        user=user,
        name=_normalize_food_name(name),
        serving=serving,
        unit=unit,
        brand=_extract_brand(food_data),
        description=food_data.get("ingredients"),
        usda_fdc_id=food_data.get("fdcId"),
    )


def search(
    term: str,
    *,
    user: User,
    page_size: int = 25,
    page_number: int = 1,
) -> list[Food]:
    """
    Search USDA FoodData Central and return Food objects.

    The USDA API returns raw food JSON records. Each record is converted
    into an unsaved Django Food instance.

    Returns:
        list[Food]:
            A list of unsaved Food objects.

    The returned Food objects are not saved to the database.
    """

    _validate_pagination(
        page_size,
        page_number,
    )

    data = _search_foods(
        term,
        page_size=page_size,
        page_number=page_number,
    )

    return [
        _create_unsaved_food(
            food,
            user=user,
        )
        for food in data.get("foods", [])
    ]


def _save_nutrients(
    food: Food,
    nutrient_data: list[dict[str, Any]],
) -> None:
    """
    Attach USDA nutrients to a saved Food.
    """

    nutrients = Nutrient.objects.filter(
        usda_nutrient_number__isnull=False,
    )

    nutrient_map = {
        nutrient.usda_nutrient_number: nutrient
        for nutrient in nutrients
    }

    for item in nutrient_data:
        nutrient = item.get("nutrient")

        if not nutrient:
            continue

        nutrient_number = str(nutrient.get("number"))

        db_nutrient = nutrient_map.get(nutrient_number)

        if not db_nutrient:
            continue

        amount = item.get("amount")

        if amount is None:
            amount = 0

        FoodNutrient.objects.create(
            food=food,
            nutrient=db_nutrient,
            amount=Decimal(str(amount)),
        )


def save_by_id(
    fdc_id: int,
    *,
    user: User,
) -> Food:
    """
    Fetch a USDA food by FDC ID and save it locally.
    """

    food_data = _get_food(fdc_id)

    food = _create_unsaved_food(
        food_data,
        user=user,
    )

    with transaction.atomic():
        food.save()

        _save_nutrients(
            food,
            food_data.get("foodNutrients", []),
        )

    return food