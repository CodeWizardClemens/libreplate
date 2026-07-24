# foods/views.py
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views import View
from django.views.decorators.http import require_POST

from diary.models import Meal, MealFood
from foods.forms import FoodForm
from foods.models import Food, FoodNutrient
from foods.services.usda_client import USDAClient
from foods.services.usda_import import import_usda_food
from nutrients.models import Nutrient
from recipes.models import Recipe, RecipeIngredient

# =============================================================================
# Helpers
# =============================================================================


def tags_modal(request, food_id):
    # TODO
    pass


def tags_save(request, food_id):
    # TODO
    pass


@login_required
@require_POST
def toggle_favorite(request, food_id):
    food = get_object_or_404(
        Food,
        id=food_id,
        user=request.user,
    )

    food.is_favorite = not food.is_favorite
    food.save(update_fields=["is_favorite"])

    response = render(
        request,
        "foods/partials/favorite_button.html",
        {
            "food": food,
        },
    )

    response["HX-Trigger"] = "foodsChanged"

    return response


def get_food_queryset(user, sort):
    foods = Food.objects.filter(user=user).prefetch_related(
        Prefetch(
            "food_nutrients",
            queryset=FoodNutrient.objects.select_related("nutrient"),
        )
    )

    if sort == "name":
        return foods.order_by("-is_favorite", "name")

    if sort == "last_used":
        return foods.order_by("-is_favorite", "-last_used_at", "-created_at")

    return foods.order_by("-is_favorite", "-created_at")


def get_visible_nutrients():
    nutrients = list(Nutrient.objects.filter(show_in_foods=True).order_by("order"))

    nutrient_lookup = {nutrient.name.lower(): nutrient for nutrient in nutrients}

    return nutrients, nutrient_lookup


def build_local_food_data(foods, nutrients, query=""):
    results = []

    for food in foods:
        if query and query.lower() not in food.name.lower():
            continue

        nutrient_map = {
            fn.nutrient_id: float(fn.amount) for fn in food.food_nutrients.all()
        }

        formatted = [
            {
                "name": nutrient.name,
                "abbr": nutrient.abbreviation,
                "value": nutrient_map.get(nutrient.id, 0),
            }
            for nutrient in nutrients
        ]

        results.append(
            {
                "id": str(food.id),
                "name": food.name,
                "description": food.description or "",
                "serving": float(food.serving),
                "unit": food.unit.name if food.unit else "",
                "nutrients": formatted,
                "source": "local",
                "brand": food.brand or "",
                "barcode": food.barcode or "",
                "is_favorite": food.is_favorite,
            }
        )

    return results


def build_usda_food_data(user, query, nutrients):
    if not query:
        return []

    client = USDAClient()
    results = []

    for food in client.search(query):
        # USDA nutrients are in food["nutrients"]
        usda_values = {n["number"]: n["value"] for n in food.get("nutrients", [])}

        formatted = [
            {
                "name": nutrient.name,
                "abbr": nutrient.abbreviation,
                "value": usda_values.get(nutrient.usda_nutrient_number, 0),
            }
            for nutrient in nutrients
        ]

        results.append(
            {
                "id": f"usda_{food['fdc_id']}",
                "fdc_id": food["fdc_id"],
                "name": food["name"],
                "description": food["description"],
                "serving": float(food["serving"]),
                "unit": food["unit"],
                "nutrients": formatted,
                "source": "usda",
                "brand": food["brand"],
                "barcode": food["barcode"],
            }
        )

    return results


def selected_foods(user, ids):
    foods = []

    for value in ids:
        if value.startswith("usda_"):
            fdc_id = int(value.split("_", 1)[1])
            food = import_usda_food(user, fdc_id)
        else:
            food = get_object_or_404(
                Food,
                user=user,
                id=int(value),
            )

        foods.append(food)

    return foods


def touch_food(food: Food):
    food.last_used_at = timezone.now()
    food.save(update_fields=["last_used_at"])


def add_foods_to_meal_instance(meal, foods):
    for food in foods:
        MealFood.objects.create(
            meal=meal,
            food=food,
            serving_size=food.serving,
            number_of_servings=1,
        )
        touch_food(food)


def save_food_form(form, user=None):
    food = form.save(commit=False)

    if user:
        food.user = user

    food.last_used_at = timezone.now()
    food.save()

    form.save_nutrients(food)

    return food


# =============================================================================
# Views
# =============================================================================


class FoodView(LoginRequiredMixin, View):
    def get(self, request):
        context = self.get_page_context(request)
        print(context)

        foods_data = self.build_foods_data(
            request.user,
            context["sorting_method"],
            context["user_food_search_query"],
            context["use_local_search"],
            context["use_usda_search"],
        )

        hidden_fields = self.build_hidden_fields(
            context["meal_id"],
            context["meal_name"],
            context["recipe_id"],
            context["recipe_name"],
        )

        return render(
            request,
            "foods/foods.html",
            {
                "foods": foods_data,
                "sort": context["sorting_method"],
                "meal_id": context["meal_id"],
                "meal_name": context["meal_name"],
                "meal_date": context["meal_date"],
                "recipe_id": context["recipe_id"],
                "recipe_name": context["recipe_name"],
                "user_food_search_query": context["user_food_search_query"],
                "use_local_search": context["use_local_search"],
                "use_usda_search": context["use_usda_search"],
                "food_sort_options": self.get_sort_options(),
                "search_hidden_fields": hidden_fields,
            },
        )

    def get_page_context(self, request):
        return {
            "sorting_method": request.GET.get("sort", "last_used"),
            "meal_id": request.GET.get("meal_id"),
            "recipe_id": request.GET.get("recipe_id"),
            "user_food_search_query": request.GET.get("q", "").strip(),
            "use_local_search": request.GET.get("use_local_search") == "1",
            "use_usda_search": request.GET.get("use_usda_search") == "1",
            "meal_name": request.GET.get("meal_name"),
            "recipe_name": request.GET.get("recipe_name"),
            "meal_date": request.GET.get("meal_date"),
            "recipe_date": request.GET.get("recipe_date"),
        }

    def build_foods_data(
        self,
        user,
        sorting_method,
        search_query,
        use_local_search,
        use_usda_search,
    ):
        nutrients, _ = get_visible_nutrients()
        foods_data = []

        if not search_query or use_local_search:
            foods_data.extend(
                build_local_food_data(
                    get_food_queryset(user, sorting_method),
                    nutrients,
                    search_query,
                )
            )

        if search_query and use_usda_search:
            try:
                foods_data.extend(
                    build_usda_food_data(
                        user,
                        search_query,
                        nutrients,
                    )
                )
            except Exception as exc:
                print("USDA search failed:", exc)

        return foods_data

    def build_hidden_fields(
        self,
        meal_id,
        meal_name,
        recipe_id,
        recipe_name,
    ):
        hidden_fields = []

        if meal_id:
            hidden_fields.extend(
                [
                    {
                        "name": "meal",
                        "value": meal_id,
                    },
                    {
                        "name": "meal_name",
                        "value": meal_name,
                    },
                ]
            )

        if recipe_id:
            hidden_fields.extend(
                [
                    {
                        "name": "recipe_id",
                        "value": recipe_id,
                    },
                    {
                        "name": "recipe_name",
                        "value": recipe_name,
                    },
                ]
            )

        return hidden_fields

    # TODO use database for this...
    def get_sort_options(self):
        return [
            {
                "value": "last_used",
                "label": "Last used",
            },
            {
                "value": "last_added",
                "label": "Last added",
            },
            {
                "value": "name",
                "label": "Name",
            },
        ]


@login_required
def import_usda_food_view(request, fdc_id):
    if request.method != "POST":
        return redirect("foods")

    food = import_usda_food(request.user, fdc_id)

    touch_food(food)

    return redirect("foods")


@login_required
def food_create(request):
    show_all = request.GET.get("all") == "1"

    if request.method == "POST":
        form = FoodForm(request.POST, show_all=show_all)

        if form.is_valid():
            save_food_form(form, request.user)
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
def food_edit(request, pk):
    food = get_object_or_404(
        Food,
        pk=pk,
        user=request.user,
    )

    show_all = request.GET.get("all") == "1"

    if request.method == "POST":
        form = FoodForm(
            request.POST,
            instance=food,
            show_all=show_all,
        )

        if form.is_valid():
            save_food_form(form)
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
@require_POST
def food_delete(request, food_id):
    recipe = get_object_or_404(
        Recipe,
        id=food_id,
        user=request.user,
    )

    recipe.delete()

    if request.headers.get("HX-Request"):
        response = render(
            request,
            "foods/partials/empty.html",
        )
        response["HX-Trigger"] = "foodsChanged"
        return response

    return redirect("foods")


@login_required
def add_foods_to_meal(request, meal_id):
    if request.method != "POST":
        return redirect("foods")

    meal = get_object_or_404(
        Meal,
        id=meal_id,
        user=request.user,
    )

    foods = selected_foods(
        request.user,
        request.POST.getlist("foods"),
    )

    add_foods_to_meal_instance(meal, foods)

    return redirect("diary_today")


@login_required
def add_foods_to_meal_direct(request, meal_id, meal_name, meal_date):

    if request.method != "POST":
        return redirect("foods")

    foods = selected_foods(
        request.user,
        request.POST.getlist("foods"),
    )
    if meal_id == "dm-1":
        meal, _ = Meal.objects.get_or_create(
            user=request.user,
            date=datetime.strptime(meal_date, "%B %d, %Y").date(),
            name=meal_name,
        )
    else:
        from diary.views import get_or_create_real_meal

        meal = get_or_create_real_meal(
            meal_id,
            request.user,
            date=timezone.localdate(),
        )

    add_foods_to_meal_instance(meal, foods)

    return redirect(
        "diary_day",
        date=meal.date.strftime("%Y-%m-%d"),
    )


@login_required
def add_foods_to_recipe_direct(request, recipe_id):
    if request.method != "POST":
        return redirect("foods")

    recipe = get_object_or_404(
        Recipe,
        id=recipe_id,
        user=request.user,
    )

    foods = selected_foods(
        request.user,
        request.POST.getlist("foods"),
    )

    order = recipe.ingredients.count()
    for food in foods:
        RecipeIngredient.objects.create(
            recipe=recipe,
            food=food,
            number_of_servings=1,
            serving_amount=food.serving,
            order=order,
        )
        touch_food(food)
        order += 1

    return redirect(
        "recipe_edit",
        recipe_id=recipe.id,
    )
