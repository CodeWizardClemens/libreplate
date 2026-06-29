from datetime import date

from django.utils import timezone
from lupa import LuaRuntime

from diary.models import Meal, MealFood
from foods.models import Food


def execute_script(script):
    runtime = LuaRuntime(
        unpack_returned_tuples=True,
    )
    globals = runtime.globals()
    user = script.user

    result = {
        "redirect": None,
    }

    def print_message(text):
        print("[LUA]", text)

    def redirect_to(url):
        result["redirect"] = str(url)

    def get_food(name):
        food = Food.objects.filter(
            user=user,
            name=name,
        ).first()

        return food.id if food else None

    def add_food_to_today(food_id, servings=1):
        meal, _ = Meal.objects.get_or_create(
            user=user,
            date=date.today(),
            name="Breakfast",
            defaults={"order": 0},
        )

        food = Food.objects.get(
            id=food_id,
            user=user,
        )

        MealFood.objects.create(
            meal=meal,
            food=food,
            serving_size=float(food.serving),
            number_of_servings=float(servings),
        )

    def create_food(name, serving=100):
        food = Food.objects.create(
            user=user,
            name=name,
            serving=serving,
        )

        return food.id

    globals.print = print_message
    globals.redirect = redirect_to
    globals.get_food = get_food
    globals.create_food = create_food
    globals.add_food_to_today = add_food_to_today

    runtime.execute(script.lua_code)

    script.last_run_at = timezone.now()
    script.save(update_fields=["last_run_at"])

    return result