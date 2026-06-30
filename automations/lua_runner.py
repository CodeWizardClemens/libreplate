from collections import defaultdict
from datetime import date, datetime, timedelta

from django.utils import timezone
from lupa import LuaRuntime

from diary.models import Meal, MealFood
from foods.models import Food
from groceries.models import GroceryList, GroceryListFood


WEEKDAYS = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6,
}


def execute_automation(automation):
    runtime = LuaRuntime(
        unpack_returned_tuples=True,
    )
    globals = runtime.globals()
    user = automation.user

    result = {
        "redirect": None,
    }

    def parse_lua_date(value):
        if isinstance(value, date):
            return value

        value = str(value).strip().lower()
        today = date.today()

        if value in ("today", "now"):
            return today

        # yyyy-mm-dd
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            pass

        # dd-mm-yyyy
        try:
            return datetime.strptime(value, "%d-%m-%Y").date()
        except ValueError:
            pass

        if value.startswith("next_"):
            weekday = WEEKDAYS[value[5:]]
            days = (weekday - today.weekday()) % 7
            if days == 0:
                days = 7
            return today + timedelta(days=days)

        if value.startswith("in_") and value.endswith("_days"):
            days = int(value[3:-5])
            return today + timedelta(days=days)

        if value.startswith("in_") and value.endswith("_weeks"):
            weeks = int(value[3:-6])
            return today + timedelta(weeks=weeks)

        raise ValueError(f"Unsupported date expression: {value}")

    # ------------------------------------------------------------------
    # Date helpers exposed to Lua
    # ------------------------------------------------------------------

    def today():
        return "today"

    def next_day(day):
        return f"next_{str(day).lower()}"

    def in_days(days):
        return f"in_{int(days)}_days"

    def in_weeks(weeks):
        return f"in_{int(weeks)}_weeks"

    # ------------------------------------------------------------------
    # Grocery list
    # ------------------------------------------------------------------

    def create_grocery_list_from_diary_entries(starting_date, ending_date):
        start = parse_lua_date(starting_date)
        end = parse_lua_date(ending_date)

        if start > end:
            raise ValueError("starting_date must be before ending_date")

        grocery_list = GroceryList.objects.create(
            user=user,
            date_start=start,
            date_end=end,
            generate_from_diary=True,
        )

        totals = defaultdict(float)

        meal_foods = (
            MealFood.objects.select_related("meal", "food")
            .filter(
                meal__user=user,
                meal__date__gte=start,
                meal__date__lte=end,
            )
        )

        for meal_food in meal_foods:
            totals[meal_food.food_id] += (
                meal_food.serving_size * meal_food.number_of_servings
            )

        foods = Food.objects.in_bulk(totals.keys())

        GroceryListFood.objects.bulk_create(
            [
                GroceryListFood(
                    grocery_list=grocery_list,
                    food=foods[food_id],
                    amount=amount,
                )
                for food_id, amount in totals.items()
            ]
        )

        return grocery_list.id

    # ------------------------------------------------------------------
    # Existing functions
    # ------------------------------------------------------------------

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

    # ------------------------------------------------------------------
    # Register globals
    # ------------------------------------------------------------------

    globals.print = print_message
    globals.redirect = redirect_to
    globals.get_food = get_food
    globals.create_food = create_food
    globals.add_food_to_today = add_food_to_today
    globals.create_grocery_list_from_diary_entries = (
        create_grocery_list_from_diary_entries
    )

    # dates namespace
    dates = runtime.table()
    dates.today = today
    dates.next = next_day
    dates.in_days = in_days
    dates.in_weeks = in_weeks

    globals.dates = dates

    runtime.execute(automation.lua_code)

    automation.last_run_at = timezone.now()
    automation.save(update_fields=["last_run_at"])

    return result