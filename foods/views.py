from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch

from .models import Food, FoodNutrient
from nutrients.models import Nutrient
from .forms import FoodForm

import requests
from django.utils import timezone
from diary.models import Meal, MealFood
from foods.models import Food

OPENFOODFACTS_URL = "https://world.openfoodfacts.org/cgi/search.pl"


@login_required
def openfood_search(request):
    query = request.GET.get("q", "")
    products = []

    if query:
        headers = {"User-Agent": "LibrePlate/1.0 (contact: dev@example.com)"}

        params = {
            "search_terms": query,
            "search_simple": 1,
            "action": "process",
            "json": 1,
            "page_size": 20,
        }

        try:
            response = requests.get(
                OPENFOODFACTS_URL, params=params, headers=headers, timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                products = data.get("products", [])

        except requests.RequestException:
            products = []

    return render(
        request, "foods/openfood_search.html", {"query": query, "products": products}
    )


@login_required
def import_openfood(request):
    if request.method == "POST":
        name = request.POST.get("name")
        barcode = request.POST.get("barcode")
        brand = request.POST.get("brand")

        if barcode and Food.objects.filter(barcode=barcode, user=request.user).exists():
            return redirect("foods")

        Food.objects.create(
            name=name or "Unknown product",
            barcode=barcode,
            brand=brand,
            user=request.user,
            serving=100,
        )

    return redirect("foods")


@login_required
def foods(request):
    sort = request.GET.get("sort", "last_used")
    meal_id = request.GET.get("meal")
    select_step = request.GET.get("select_step")  # NEW

    foods_qs = Food.objects.filter(user=request.user).prefetch_related(
        Prefetch(
            "food_nutrients", queryset=FoodNutrient.objects.select_related("nutrient")
        )
    )

    if sort == "name":
        foods_qs = foods_qs.order_by("name")

    elif sort == "last_used":
        foods_qs = foods_qs.order_by("-last_used_at", "-created_at")

    else:
        foods_qs = foods_qs.order_by("-created_at")

    nutrients = list(Nutrient.objects.filter(show_in_foods=True).order_by("order"))

    foods_data = []

    for food in foods_qs:
        nutrient_map = {fn.nutrient_id: fn.amount for fn in food.food_nutrients.all()}

        formatted_nutrients = []

        for nutrient in nutrients:
            formatted_nutrients.append(
                {
                    "name": nutrient.name,
                    "abbr": nutrient.abbreviation,
                    "value": float(nutrient_map.get(nutrient.id, 0)),
                }
            )

        foods_data.append(
            {
                "id": food.id,
                "name": food.name,
                "description": food.description or "",
                "serving": float(food.serving),
                "unit": food.unit.name if food.unit else "",
                "nutrients": formatted_nutrients,
            }
        )

    return render(
        request,
        "foods/foods.html",
        {
            "foods": foods_data,
            "nutrients": nutrients,
            "sort": sort,
            "meal_id": meal_id,
            "select_step": select_step,  # NEW
        },
    )


@login_required
def create_food(request):
    show_all = request.GET.get("all") == "1"

    if request.method == "POST":
        form = FoodForm(request.POST, show_all=show_all)

        if form.is_valid():
            food = form.save(commit=False)
            food.user = request.user
            food.last_used_at = timezone.now()
            food.save()

            form.save_nutrients(food)

            return redirect("foods")
    else:
        form = FoodForm(show_all=show_all)

    return render(
        request,
        "foods/food_form.html",
        {
            "form": form,
            "show_all": show_all,
        },
    )


@login_required
def edit_food(request, pk):
    food = get_object_or_404(Food, pk=pk, user=request.user)

    show_all = request.GET.get("all") == "1"

    if request.method == "POST":
        form = FoodForm(
            request.POST,
            instance=food,
            show_all=show_all,
        )

        if form.is_valid():
            food = form.save(commit=False)
            food.last_used_at = timezone.now()
            food.save()
            form.save()
            return redirect("foods")
    else:
        form = FoodForm(
            instance=food,
            show_all=show_all,
        )

    return render(
        request,
        "foods/food_form.html",
        {
            "form": form,
            "show_all": show_all,
        },
    )


@login_required
def delete_food(request, pk):
    food = get_object_or_404(Food, pk=pk, user=request.user)

    if request.method == "POST":
        food.delete()
        return redirect("foods")

    return render(request, "foods/food_confirm_delete.html", {"food": food})


def select_meal(request):
    if request.method != "POST":
        return redirect("foods")

    food_ids = request.POST.getlist("foods")

    foods = Food.objects.filter(
        user=request.user,
        id__in=food_ids,
    )

    meals = Meal.objects.filter(
        user=request.user,
        date=timezone.localdate(),
    )

    return render(
        request,
        "foods/select_meal.html",
        {
            "foods": foods,
            "food_ids": food_ids,
            "meals": meals,
        },
    )


def add_foods_to_meal(request, meal_id):
    if request.method != "POST":
        return redirect("foods")

    meal = get_object_or_404(
        Meal,
        id=meal_id,
        user=request.user,
    )

    food_ids = request.POST.getlist("foods")

    foods = Food.objects.filter(
        user=request.user,
        id__in=food_ids,
    )

    for food in foods:
        MealFood.objects.create(
            meal=meal,
            food=food,
            serving_size=food.serving,
            number_of_servings=1,
        )
        food.last_used_at = timezone.now()
        food.save(update_fields=["last_used_at"])
    return redirect("diary_today")


@login_required
def add_foods_to_meal_direct(request, meal_id):
    if request.method != "POST":
        return redirect("foods")

    from diary.views import get_or_create_real_meal

    meal = get_or_create_real_meal(
        meal_id,
        request.user,
        date=timezone.localdate(),
    )

    food_ids = request.POST.getlist("foods")

    foods = Food.objects.filter(
        user=request.user,
        id__in=food_ids,
    )

    for food in foods:
        MealFood.objects.create(
            meal=meal,
            food=food,
            serving_size=food.serving,
            number_of_servings=1,
        )

        food.last_used_at = timezone.now()
        food.save(update_fields=["last_used_at"])

    return redirect("diary_day", date=meal.date.strftime("%Y-%m-%d"))
