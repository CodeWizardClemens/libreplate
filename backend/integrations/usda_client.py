from __future__ import annotations

from decimal import Decimal
from functools import lru_cache
from typing import Any, Literal

import requests
from django.contrib.auth.models import User
from django.db import transaction
from pydantic import (
    AliasChoices,
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)

from foods.models import Food, FoodNutrient
from integrations.models import USDAAPISettings
from nutrients.models import Nutrient
from units.models import Unit

USDA_API_BASE_URL = "https://api.nal.usda.gov/fdc/v1"

MIN_PAGE_SIZE = 1
MAX_PAGE_SIZE = 50
MIN_PAGE_NUMBER = 1
MAX_PAGE_NUMBER = 1000

USDADataType = Literal[
    "Branded",
    "Foundation",
    "SR Legacy",
    "Survey (FNDDS)",
    "Experimental",
]

DEFAULT_NON_BRANDED_DATA_TYPES: tuple[USDADataType, ...] = (
    "Foundation",
    "SR Legacy",
    "Survey (FNDDS)",
    "Experimental",
)


class USDAError(Exception):
    """Raised when the USDA API cannot be queried successfully."""


class USDAFoodNutrient(BaseModel):
    id: int = Field(alias="nutrientId")
    # Can also be None or a sub number, so has to be a decimal and None.
    # This is not stated in document above.
    number: Decimal | None = Field(default=None, alias="nutrientNumber")
    name: str = Field(alias="nutrientName")
    unit_name: str = Field(alias="unitName")
    value: Decimal = Decimal("0")

    model_config = ConfigDict(populate_by_name=True)

    @model_validator(mode="before")
    @classmethod
    def _flatten_nested_nutrient(cls, data: Any) -> Any:
        """Normalize the two shapes the USDA API returns foodNutrients in.

        Branded foods use a flattened shape:
            {"nutrientId": 1003, "nutrientName": "Protein",
             "nutrientNumber": "203", "unitName": "g", "value": 20.1}

        Foundation / SR Legacy / Survey (FNDDS) / Experimental foods nest
        the nutrient info under a "nutrient" sub-object instead, and use
        "amount" rather than "value":
            {"type": "FoodNutrient", "id": 123456,
             "nutrient": {"id": 1003, "number": "203", "name": "Protein",
                           "unitName": "g"},
             "amount": 20.1}
        """
        if not isinstance(data, dict):
            return data

        data = dict(data)
        nested = data.get("nutrient")
        if isinstance(nested, dict):
            data.setdefault("nutrientId", nested.get("id"))
            data.setdefault("nutrientNumber", nested.get("number"))
            data.setdefault("nutrientName", nested.get("name"))
            data.setdefault("unitName", nested.get("unitName"))

        # Nested-format entries use "amount" instead of "value"
        if "amount" in data and "value" not in data:
            data["value"] = data["amount"]

        return data

    @field_validator("number", mode="before")
    @classmethod
    def empty_string_to_none(cls, value):
        if value == "":
            return None
        return value

    @field_validator("value", mode="before")
    @classmethod
    def coerce_value(cls, value):
        # Some entries have non-numeric/empty amounts (e.g. "" or None
        # for nutrients with no measured amount). Treat those as 0 rather
        # than failing validation for the whole food.
        if value in (None, ""):
            return Decimal("0")
        try:
            return Decimal(str(value))
        except Exception:
            return Decimal("0")


class USDAFood(BaseModel):
    name: str = Field(alias="description")
    serving: float = 100
    unit_name: str = "g"
    brand: str | None = Field(None, validation_alias="brandName")
    description: str | None = None
    fdc_id: int | None = Field(
        None,
        validation_alias=AliasChoices("fdc_id", "fdcId"),
    )
    data_type: str | None = Field(
        None,
        validation_alias=AliasChoices("data_type", "dataType"),
    )
    food_nutrients: list[USDAFoodNutrient] = Field(
        default_factory=list,
        alias="foodNutrients",
    )

    model_config = ConfigDict(populate_by_name=True)

    @field_validator("food_nutrients", mode="before")
    @classmethod
    def _drop_invalid_nutrients(cls, value: Any) -> Any:
        """Drop any foodNutrient entries that can't be parsed/coerced
        (e.g. missing id/name/unit even after normalization, or values
        that can't be converted to int/float) instead of failing
        validation for the entire food.
        """
        if not isinstance(value, list):
            return value

        valid: list[USDAFoodNutrient] = []
        for item in value:
            try:
                valid.append(USDAFoodNutrient.model_validate(item))
            except Exception:
                continue
        return valid

    def to_food(self, *, user: User, unit: Unit | None) -> Food:
        return Food(
            user=user,
            name=_normalize_text(self.name) or "Unknown food",
            serving=self.serving,
            unit=unit,
            brand=_normalize_text(self.brand),
            description=_normalize_text(self.description),
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
    print(response.url)
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
    data_type: tuple[USDADataType, ...] = DEFAULT_NON_BRANDED_DATA_TYPES,
) -> dict[str, Any]:
    return _request(
        "foods/search",
        params={
            "generalSearchInput": term,
            "pageSize": page_size,
            "pageNumber": page_number,
            "dataType": list(data_type),
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

    return Unit.objects.filter(
        name=unit_name,
    ).first()


def _extract_brand(food: dict[str, Any]) -> str | None:
    return food.get("brandOwner") or food.get("brandName")


def _create_usda_food(
    food_data: dict[str, Any],
) -> USDAFood:
    data = food_data.copy()
    data.update(
        name=food_data.get("description"),
        brand=_extract_brand(food_data),
        description=(food_data.get("ingredients") or food_data.get("description")),
    )
    return USDAFood(**data)


def search(
    term: str,
    *,
    page_size: int = 25,
    page_number: int = 1,
    data_type: tuple[USDADataType, ...] = DEFAULT_NON_BRANDED_DATA_TYPES,
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
            data_type=data_type,
        ).get("foods", [])
    ]


def _save_nutrients(
    food: Food,
    nutrient_data: list[USDAFoodNutrient],
) -> None:
    nutrient_map = {
        nutrient.usda_nutrient_number: nutrient
        for nutrient in Nutrient.objects.filter(
            usda_nutrient_number__isnull=False,
        )
    }
    food_nutrients = [
        FoodNutrient(
            food=food,
            nutrient=nutrient_map[item.number],
            amount=item.value,
        )
        for item in nutrient_data
        if item.number is not None and item.number in nutrient_map
    ]
    FoodNutrient.objects.bulk_create(food_nutrients)


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
