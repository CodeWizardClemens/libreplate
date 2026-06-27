from datetime import datetime, timedelta
from collections import defaultdict
import json

from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import Meal, MealFood
from settings.models import DefaultMeal
from .forms import MealForm, MealFoodForm, AddMealFoodForm

from nutrients.models import Nutrient
from foods.models import Food

from body_metrics.models import BodyMetric, BodyMetricLog
from common.food_selection import get_user_foods

from collections import defaultdict

import json
from goals.models import GoalGroup, GoalNutrient

class VirtualMealFoodManager:
    def all(self):
        return []

def get_active_goal_group(user, selected_date):
    """
    Returns the single GoalGroup active for the selected_date.
    Rules:
    - start_date is optional (None = -infinity)
    - end_date is optional (None = +infinity)
    - date must be within inclusive range
    """

    groups = GoalGroup.objects.filter(user=user)

    for g in groups:
        start_ok = g.start_date is None or g.start_date <= selected_date
        end_ok = g.end_date is None or g.end_date >= selected_date

        if start_ok and end_ok:
            return g

    return None

def to_int_dict(d):
    return {k: int(v) for k, v in d.items()}

def calculate_meal_food_totals(meal_food):
    """
    Calculate nutrients for a single MealFood.
    Formula:
        nutrient_per_100g * serving_size * servings / 100
    """
    totals = defaultdict(float)

    serving_size = float(meal_food.serving_size or 0)
    servings = float(meal_food.number_of_servings or 0)

    for fn in meal_food.food.food_nutrients.all():
        totals[fn.nutrient_id] += (
            float(fn.amount)
            * serving_size
            * servings
            / 100
        )

    return totals


def calculate_meal_totals(meal):
    totals = defaultdict(float)

    for meal_food in meal.meal_foods.all():
        food_totals = calculate_meal_food_totals(meal_food)

        meal_food.nutrient_values = to_int_dict(food_totals)

        for nutrient_id, value in food_totals.items():
            totals[nutrient_id] += value

    meal.total_nutrients = to_int_dict(totals)

    return totals


def calculate_day_totals(meals):
    totals = defaultdict(float)

    for meal in meals:
        if isinstance(meal, VirtualMeal):
            continue

        meal_totals = calculate_meal_totals(meal)

        for nutrient_id, value in meal_totals.items():
            totals[nutrient_id] += value

    return to_int_dict(totals)


class VirtualMeal:
    """
    Represents a default meal that does NOT yet exist in DB.
    Will be materialized into a real Meal only when user edits it.
    """

    def __init__(self, default_meal, date, user):
        self.id = f"dm-{default_meal.id}"
        self.default_meal = default_meal
        self.name = default_meal.name
        self.date = date
        self.user = user

        self.note = ""
        self.order = default_meal.order

        self.meal_foods = VirtualMealFoodManager()
        self.total_nutrients = defaultdict(float)
        self.has_foods = False

        self.is_virtual = True
        self.is_default = True


def get_or_create_real_meal(meal_id, user, date=None):
    """
    Resolves either:
    - real Meal (int id)
    - virtual default meal (dm-<id>) -> creates Meal on demand
    """

    # REAL MEAL
    if isinstance(meal_id, int) or (isinstance(meal_id, str) and meal_id.isdigit()):
        return get_object_or_404(Meal, id=int(meal_id), user=user)

    # DEFAULT MEAL
    if isinstance(meal_id, str) and meal_id.startswith("dm-"):
        default_id = int(meal_id.replace("dm-", ""))
        default = get_object_or_404(DefaultMeal, id=default_id, user=user)

        meal, created = Meal.objects.get_or_create(
            user=user,
            date=date,
            name=default.name,
            defaults={
                "order": default.order,
                "note": "",
            },
        )
        return meal

    raise ValueError("Invalid meal id")


# =========================================================
# MAIN DIARY VIEW
# =========================================================
def diary_day(request, date=None):

    if date:
        selected_date = datetime.strptime(date, "%Y-%m-%d").date()
    else:
        selected_date = timezone.localdate()

    week_start = selected_date - timedelta(days=selected_date.weekday())

    week_days = []
    for i in range(7):
        day = week_start + timedelta(days=i)
        week_days.append(
            {
                "date": day,
                "is_today": day == timezone.localdate(),
                "is_selected": day == selected_date,
            }
        )

    real_meals = (
        Meal.objects.filter(date=selected_date, user=request.user)
        .prefetch_related(
            "meal_foods",
            "meal_foods__food",
            "meal_foods__food__food_nutrients",
            "meal_foods__food__food_nutrients__nutrient",
        )
        .order_by("order")
    )

    meal_map = {m.name: m for m in real_meals}

    meals = []

    for dm in DefaultMeal.objects.filter(user=request.user).order_by("order"):

        if dm.name in meal_map:
            meal = meal_map[dm.name]
            meal.is_virtual = False
            meal.is_default = True
        else:
            meal = VirtualMeal(dm, selected_date, request.user)

        meals.append(meal)

    day_total = calculate_day_totals(meals)

    # ----------------------------
    # GOALS
    # ----------------------------
    goal_group = get_active_goal_group(request.user, selected_date)

    goal_nutrients = {}

    if goal_group:
        goal_qs = GoalNutrient.objects.filter(goal_group=goal_group)

        goal_nutrients = {
            g.nutrient_id: float(g.amount)
            for g in goal_qs
        }

    body_metrics = BodyMetric.objects.filter(
        show_in_diary_total=True
    ).order_by("order")

    logs = BodyMetricLog.objects.filter(
        user=request.user,
        date=selected_date,
    )

    log_map = {log.body_metric_id: log.amount for log in logs}

    context = {
        "selected_date": selected_date,
        "meals": meals,
        "meal_form": MealForm(),
        "week_days": week_days,
        "yesterday": selected_date - timedelta(days=1),
        "tomorrow": selected_date + timedelta(days=1),
        "month_name": selected_date.strftime("%B %Y"),
        "nutrients_total": Nutrient.objects.filter(
            show_in_diary_total=True
        ).order_by("order"),
        "nutrients_meal": Nutrient.objects.filter(
            show_in_diary_meal=True
        ).order_by("order"),
        "day_total": day_total,
        "goal_nutrients": to_int_dict(goal_nutrients),
        "body_metrics": body_metrics,
        "log_map": log_map,
    }

    return render(request, "diary/day.html", context)

# =========================================================
# MEALS
# =========================================================
def add_meal(request, date):

    if request.method == "POST":

        form = MealForm(request.POST)

        if form.is_valid():
            meal = form.save(commit=False)
            meal.user = request.user
            meal.date = datetime.strptime(date, "%Y-%m-%d").date()

            last_order = (
                Meal.objects.filter(date=meal.date, user=request.user)
                .order_by("-order")
                .values_list("order", flat=True)
                .first()
            )

            meal.order = (last_order + 1) if last_order is not None else 0
            meal.save()

    return redirect("diary_day", date=date)


def delete_meal(request, meal_id):

    if isinstance(meal_id, str) and meal_id.startswith("dm-"):
        return redirect("diary_today")

    meal = get_object_or_404(Meal, id=meal_id)

    date = meal.date.strftime("%Y-%m-%d")

    if request.method == "POST":
        meal.delete()

    return redirect("diary_day", date=date)


# =========================================================
# MEAL FOOD
# =========================================================
def add_food_to_meal(request, meal_id):

    meal = get_or_create_real_meal(meal_id, request.user, date=datetime.today().date())

    if request.method == "POST":

        form = MealFoodForm(request.POST)

        form.fields["food"].queryset = Food.objects.filter(user=request.user).order_by(
            "name"
        )

        if form.is_valid():
            meal_food = form.save(commit=False)
            meal_food.meal = meal
            meal_food.save()

    return redirect("diary_day", date=meal.date.strftime("%Y-%m-%d"))


def delete_meal_food(request, meal_food_id):

    meal_food = get_object_or_404(MealFood, id=meal_food_id)
    date = meal_food.meal.date.strftime("%Y-%m-%d")

    if request.method == "POST":
        meal_food.delete()

    return redirect("diary_day", date=date)


# =========================================================
# MEAL NOTE
# =========================================================
def update_note(request, meal_id):

    meal = get_or_create_real_meal(meal_id, request.user, date=datetime.today().date())

    if request.method == "POST":
        meal.note = request.POST.get("note", "")
        meal.save()

    return redirect("diary_day", date=meal.date.strftime("%Y-%m-%d"))


# =========================================================
# BODY METRICS
# =========================================================
@require_POST
def save_body_metric(request):

    data = json.loads(request.body)

    metric_id = data.get("metric_id")
    date = data.get("date")
    amount = data.get("amount")

    if amount in ("", None):
        return JsonResponse({"ok": True})

    log, created = BodyMetricLog.objects.update_or_create(
        user=request.user,
        body_metric_id=metric_id,
        date=date,
        defaults={"amount": amount},
    )

    return JsonResponse(
        {
            "ok": True,
            "created": created,
            "amount": log.amount,
        }
    )


@require_POST
def update_meal_food(request):

    data = json.loads(request.body)

    meal_food = get_object_or_404(
        MealFood,
        id=data["meal_food_id"],
        meal__user=request.user,
    )

    meal_food.serving_size = float(data.get("serving_size") or 0)
    meal_food.number_of_servings = float(data.get("number_of_servings") or 0)
    meal_food.save()

    meal = meal_food.meal

    meal_food_totals = calculate_meal_food_totals(meal_food)

    meal_totals = calculate_meal_totals(meal)

    all_meals = (
        Meal.objects.filter(
            user=request.user,
            date=meal.date,
        )
        .prefetch_related(
            "meal_foods__food__food_nutrients"
        )
    )

    day_totals = calculate_day_totals(all_meals)

    return JsonResponse(
        {
            "ok": True,
            "meal_food": {
                str(meal_food.id): to_int_dict(meal_food_totals)
            },
            "meal": to_int_dict(meal_totals),
            "day": day_totals,
        }
    )


@require_POST
def update_note(request, meal_id):

    meal = get_or_create_real_meal(
        meal_id,
        request.user,
        date=datetime.today().date(),
    )

    data = json.loads(request.body)

    meal.note = data.get("note", "")
    meal.save()

    return JsonResponse({"ok": True})
