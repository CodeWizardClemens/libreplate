from __future__ import annotations

from decimal import Decimal
from functools import lru_cache
from typing import Any

import requests
from django.contrib.auth.models import User
from django.db import transaction
from pydantic import AliasChoices, BaseModel, ConfigDict, Field

from foods.models import Food, FoodNutrient
from integrations.models import USDAAPISettings
from nutrients.models import Nutrient
from units.models import Unit, UnitScope

USDA_API_BASE_URL = "https://api.nal.usda.gov/fdc/v1"

MIN_PAGE_SIZE = 1
MAX_PAGE_SIZE = 50
MIN_PAGE_NUMBER = 1
MAX_PAGE_NUMBER = 1000


class USDAError(Exception):
    """Raised when the USDA API cannot be queried successfully."""


class USDAFoodNutrient(BaseModel):
    amount: Decimal = Decimal("0")
    nutrient_number: str | None = Field(None, alias="number")
    nutrient_name: str | None = Field(None, alias="name")

    model_config = ConfigDict(populate_by_name=True)


class USDAFood(BaseModel):
    name: str = Field(alias="description")
    serving: float = 100
    unit_name: str = "g"

    brand: str | None = None
    description: str | None = None

    # Camelcase alias is defined to match FDC API.
    fdc_id: int | None = Field(
        None,
        validation_alias=AliasChoices("fdc_id", "fdcId"),
    )
    data_type: str | None = Field(
        None,
        validation_alias=AliasChoices("data_type", "dataType"),
    )

    food_nutrients: list[dict[str, Any]] = Field(
        default_factory=list,
        alias="foodNutrients",
    )

    model_config = ConfigDict(populate_by_name=True)

    def to_food(
        self,
        *,
        user: User,
        unit: Unit | None,
    ) -> Food:
        return Food(
            user=user,
            name=_normalize_text(self.name) or "Unknown food",
            serving=self.serving,
            unit=unit,
            brand=_normalize_text(self.brand),
            description=self.description,
            usda_fdc_id=self.fdc_id,
        )


def _validate_pagination(
    page_size: int,
    page_number: int,
) -> None:
    if not MIN_PAGE_SIZE <= page_size <= MAX_PAGE_SIZE:
        raise USDAError(
            f"page_size must be between {MIN_PAGE_SIZE} and {MAX_PAGE_SIZE}."
        )

    if not MIN_PAGE_NUMBER <= page_number <= MAX_PAGE_NUMBER:
        raise USDAError(
            f"page_number must be between {MIN_PAGE_NUMBER} and {MAX_PAGE_NUMBER}."
        )


def _normalize_text(value: str | None) -> str | None:
    if not value:
        return None

    return value.capitalize() if value.isupper() else value


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
    response = requests.get(
        f"{USDA_API_BASE_URL}/{endpoint}",
        params={
            **(params or {}),
            "api_key": _get_api_key(),
        },
        timeout=10,
    )

    if response.status_code == 404:
        raise USDAError("Food not found.")

    if not response.ok:
        raise USDAError(f"USDA API error: {response.status_code} {response.text}")

    print(response.json())
    return response.json()


@lru_cache(maxsize=128)
def _search_foods(
    term: str,
    *,
    page_size: int = 25,
    page_number: int = 1,
) -> dict[str, Any]:
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
    return _request(f"food/{fdc_id}")


def _get_global_unit(name: str) -> Unit | None:
    mappings = {
        "g": "Gram",
        "gram": "Gram",
        "grams": "Gram",
        "ml": "Milliliter",
        "milliliter": "Milliliter",
        "milliliters": "Milliliter",
    }

    unit_name = mappings.get(name.lower())

    if not unit_name:
        return None

    try:
        scope = UnitScope.objects.get(user=None)
    except UnitScope.DoesNotExist:
        return None

    return Unit.objects.filter(
        scope=scope,
        name=unit_name,
    ).first()


def _extract_brand(food: dict[str, Any]) -> str | None:
    return food.get("brandOwner") or food.get("brandName")


def _create_usda_food(
    food_data: dict[str, Any],
) -> USDAFood:
    data = food_data.copy()

    data.update(
        brand=_extract_brand(food_data),
        description=(food_data.get("ingredients") or food_data.get("description")),
    )

    return USDAFood(**data)


def search(
    term: str,
    *,
    page_size: int = 25,
    page_number: int = 1,
) -> list[USDAFood]:
    _validate_pagination(
        page_size,
        page_number,
    )

    return [
        _create_usda_food(food)
        for food in _search_foods(
            term,
            page_size=page_size,
            page_number=page_number,
        ).get("foods", [])
    ]


def _save_nutrients(
    food: Food,
    nutrient_data: list[dict[str, Any]],
) -> None:
    nutrient_map = {
        nutrient.usda_nutrient_number: nutrient
        for nutrient in Nutrient.objects.filter(
            usda_nutrient_number__isnull=False,
        )
    }

    for item in nutrient_data:
        nutrient = item.get("nutrient")

        if not nutrient:
            continue

        db_nutrient = nutrient_map.get(str(nutrient.get("number")))

        if not db_nutrient:
            continue

        FoodNutrient.objects.create(
            food=food,
            nutrient=db_nutrient,
            amount=Decimal(str(item.get("amount", 0))),
        )


def save_by_id(
    fdc_id: int,
    *,
    user: User,
) -> Food:
    raw_food = _get_food(fdc_id)

    usda_food = _create_usda_food(raw_food)

    food = usda_food.to_food(
        user=user,
        unit=_get_global_unit(usda_food.unit_name),
    )

    with transaction.atomic():
        food.save()
        _save_nutrients(
            food,
            usda_food.food_nutrients,
        )

    return food
