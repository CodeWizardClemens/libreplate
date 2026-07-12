from pydantic import BaseModel
from typing import Optional


class NutrientSchema(BaseModel):
    name: str
    description: Optional[str] = None
    abbreviation: Optional[str] = None

    show_in_diary_total: bool = False
    show_in_diary_meal: bool = False
    show_in_food_edit: bool = False
    show_in_recipe: bool = False
    show_in_foods: bool = False
    show_in_goal_edit: bool = False

    usda_nutrient_number: Optional[str] = None
    order: int = 0


def nutrient_everywhere(**kwargs):
    return NutrientSchema(
        show_in_diary_total=True,
        show_in_diary_meal=True,
        show_in_food_edit=True,
        show_in_recipe=True,
        show_in_foods=True,
        show_in_goal_edit=True,
        **kwargs,
    )


def nutrient_recipe_food_edit(**kwargs):
    return NutrientSchema(
        show_in_food_edit=True,
        show_in_recipe=True,
        **kwargs,
    )


DEFAULT_NUTRIENTS = [
    nutrient_everywhere(
        name="Calories",
        description="Energy provided by food.",
        abbreviation="kcal",
        usda_nutrient_number="1008",
        order=1,
    ),
    nutrient_everywhere(
        name="Protein",
        description="Total protein content.",
        abbreviation="g",
        usda_nutrient_number="1003",
        order=2,
    ),
    nutrient_everywhere(
        name="Carbohydrates",
        description="Total carbohydrate content.",
        abbreviation="g",
        usda_nutrient_number="1005",
        order=3,
    ),
    nutrient_everywhere(
        name="Fat",
        description="Total fat content.",
        abbreviation="g",
        usda_nutrient_number="1004",
        order=4,
    ),
    nutrient_recipe_food_edit(
        name="Fiber",
        description="Dietary fiber content.",
        abbreviation="g",
        usda_nutrient_number="1079",
        order=5,
    ),
    nutrient_recipe_food_edit(
        name="Sugar",
        description="Total sugars.",
        abbreviation="g",
        usda_nutrient_number="2000",
        order=6,
    ),
    nutrient_recipe_food_edit(
        name="Saturated Fat",
        description="Saturated fatty acids.",
        abbreviation="g",
        usda_nutrient_number="1258",
        order=7,
    ),
    nutrient_recipe_food_edit(
        name="Sodium",
        description="Sodium content.",
        abbreviation="mg",
        usda_nutrient_number="1093",
        order=8,
    ),
]