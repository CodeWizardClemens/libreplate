from django.utils import timezone

from diary.models import Meal, MealFood
from foods.models import Food


def execute_add_food_to_diary(user, config):

    food = Food.objects.get(id=config["food_id"], user=user)

    amount = config.get("amount", 1)
    meal_name = config.get("meal", "breakfast")

    meal, _ = Meal.objects.get_or_create(
        user=user, date=timezone.localdate(), name=meal_name
    )

    MealFood.objects.create(
        meal=meal, food=food, serving_size=food.serving, number_of_servings=amount
    )


EXECUTORS = {"add_food_to_diary": execute_add_food_to_diary}
