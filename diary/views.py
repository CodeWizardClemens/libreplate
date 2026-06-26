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

# =========================================================
# Helpers: virtual/default meal handling
# =========================================================
    
class VirtualMealFoodManager:
    def all(self):
        return []

def to_int_dict(d):
    return {k: int(v) for k, v in d.items()}

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


    day_total = defaultdict(float)

    # build lookup for real meals
    meal_map = {m.name: m for m in real_meals}

    meals = []

    # DEFAULT + REAL MERGE
    default_meals = DefaultMeal.objects.filter(user=request.user)

    for dm in default_meals:

        if dm.name in meal_map:
            meal = meal_map[dm.name]
            meal.is_virtual = False
            meal.is_default = True
        else:
            meal = VirtualMeal(dm, selected_date, request.user)

        meals.append(meal)

    # process nutrients for real meals only
    for meal in meals:

        meal.total_nutrients = defaultdict(float)

        meal.has_foods = False

        if hasattr(meal, "meal_foods") and not isinstance(meal, VirtualMeal):

            for meal_food in meal.meal_foods.all():
                meal.has_foods = True

                food_totals = defaultdict(float)

                for food_nutrient in meal_food.food.food_nutrients.all():
                    nutrient = food_nutrient.nutrient
                    value = float(food_nutrient.amount) * meal_food.number_of_servings

                    food_totals[nutrient.id] += value
                    meal.total_nutrients[nutrient.id] += value
                    day_total[nutrient.id] += value

                meal_food.nutrient_values = to_int_dict(food_totals)

    body_metrics = BodyMetric.objects.filter(show_in_diary_total=True).order_by("order")

    logs = BodyMetricLog.objects.filter(user=request.user, date=selected_date)

    log_map = {log.body_metric_id: log.amount for log in logs}

    context = {
        "selected_date": selected_date,
        "meals": meals,
        "meal_form": MealForm(),
        "week_days": week_days,
        "yesterday": selected_date - timedelta(days=1),
        "tomorrow": selected_date + timedelta(days=1),
        "month_name": selected_date.strftime("%B %Y"),
        "nutrients_total": Nutrient.objects.filter(show_in_diary_total=True).order_by("order"),
        "nutrients_meal": Nutrient.objects.filter(show_in_diary_meal=True).order_by("order"),
        "day_total": to_int_dict(day_total),
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

    # -----------------------------
    # Calculation helper
    # -----------------------------
    def calc_value(fn, mf):
        return (
            float(fn.amount)
            * float(mf.serving_size)
            * float(mf.number_of_servings)
            / 100
        )

    # -----------------------------
    # RAW ACCUMULATORS
    # -----------------------------
    meal_food_totals = defaultdict(float)
    meal_totals = defaultdict(float)
    day_totals = defaultdict(float)

    # =========================================================
    # 1. ROW (meal_food only)
    # =========================================================
    for fn in meal_food.food.food_nutrients.all():
        meal_food_totals[fn.nutrient_id] += calc_value(fn, meal_food)

    # =========================================================
    # 2. MEAL TOTALS
    # =========================================================
    for mf in meal.meal_foods.all():
        for fn in mf.food.food_nutrients.all():
            meal_totals[fn.nutrient_id] += calc_value(fn, mf)

    # =========================================================
    # 3. DAY TOTALS
    # =========================================================
    all_meals = Meal.objects.filter(
        user=request.user,
        date=meal.date
    ).prefetch_related(
        "meal_foods__food__food_nutrients"
    )

    for m in all_meals:
        for mf in m.meal_foods.all():
            for fn in mf.food.food_nutrients.all():
                day_totals[fn.nutrient_id] += calc_value(fn, mf)

    # =========================================================
    # FINAL RESPONSE (ALL INT SAFE)
    # =========================================================
    return JsonResponse({
        "ok": True,

        # per meal_food row
        "meal_food": {
            str(meal_food.id): to_int_dict(meal_food_totals)
        },

        # meal totals
        "meal": to_int_dict(meal_totals),

        # day totals
        "day": to_int_dict(day_totals),
    })

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