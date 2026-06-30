from collections import defaultdict
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from diary.models import Meal, MealFood
from foods.models import FoodNutrient
from nutrients.models import Nutrient

from .forms import AddRecipeToDiaryForm, RecipeForm, RecipeIngredientForm
from .models import Recipe, RecipeIngredient


def selected_recipes(user, ids):
    return Recipe.objects.filter(
        user=user,
        id__in=ids,
    ).prefetch_related("ingredients__food")


@login_required
def recipes(request):

    meal_id = request.GET.get("meal_id")
    meal_name = request.GET.get("meal_name")
    meal_date = request.GET.get("meal_date")
    recipes = Recipe.objects.filter(user=request.user)

    return render(
        request,
        "recipes/recipes.html",
        {
            "recipes": recipes,
            "meal_id": meal_id,
            "meal_name": meal_name,
            "meal_date": meal_date,
        },
    )


@login_required
def add_recipes_to_meal_direct(request, meal_id, meal_name, meal_date):
    if request.method != "POST":
        return redirect("recipes")

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

    recipes = Recipe.objects.filter(
        user=request.user,
        id__in=request.POST.getlist("recipes"),
    ).prefetch_related("ingredients__food")

    notes = []

    for recipe in recipes:
        # Add all ingredients
        for ingredient in recipe.ingredients.all():
            MealFood.objects.create(
                meal=meal,
                food=ingredient.food,
                serving_size=ingredient.serving_amount,
                number_of_servings=ingredient.default_servings,
            )

        # Collect recipe instructions
        notes.append(f"Recipe: {recipe.name}")
        if recipe.summary:
            notes.append(f"Description: {recipe.summary}")
        if recipe.instructions:
            notes.append(f"\n{recipe.instructions.strip()}")

    # Append instructions to the meal note
    if notes:
        if meal.note:
            meal.note += "\n\n"
        meal.note += "\n\n".join(notes)
        meal.save(update_fields=["note"])

    return redirect(
        "diary_day",
        date=meal.date.strftime("%Y-%m-%d"),
    )


def recipe_create(request):

    if request.method == "POST":
        form = RecipeForm(request.POST)

        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user
            recipe.last_used_at = timezone.localdate()
            recipe.save()

            if "add_food" in request.POST:
                return redirect(
                    f"/foods/?recipe_id={recipe.id}&recipe_name={recipe.name}"
                )

            return redirect("recipes")

    else:
        form = RecipeForm()

    return render(
        request,
        "recipes/recipe_edit.html",
        {
            "recipe": None,
            "form": form,
            "ingredients": [],
            "ingredient_form": None,
            "visible_nutrients": [],
        },
    )


def get_recipe(user, recipe_id):
    return get_object_or_404(
        Recipe,
        id=recipe_id,
        user=user,
    )


def update_recipe_ingredients(recipe, post_data):
    for ingredient in recipe.ingredients.all():

        serving_amount = post_data.get(f"serving_amount_{ingredient.id}")
        default_servings = post_data.get(f"default_servings_{ingredient.id}")

        if serving_amount is not None:
            ingredient.serving_amount = float(serving_amount)

        if default_servings is not None:
            ingredient.default_servings = float(default_servings)

        ingredient.save(
            update_fields=[
                "serving_amount",
                "default_servings",
            ]
        )


def handle_recipe_edit_post(request, recipe):
    form = RecipeForm(request.POST, instance=recipe)

    if not form.is_valid():
        return form, None

    form.save()
    update_recipe_ingredients(recipe, request.POST)

    if "add_food" in request.POST:
        return (
            form,
            redirect(f"/foods/?recipe_id={recipe.id}&recipe_name={recipe.name}"),
        )

    return form, redirect("recipes")


def get_recipe_context(recipe, form, user):
    visible_nutrients = list(
        Nutrient.objects.filter(show_in_recipe=True).order_by("order")
    )

    visible_ids = {n.id for n in visible_nutrients}

    ingredients = list(recipe.ingredients.select_related("food"))

    # Fetch all nutrient values for all foods in one query
    food_ids = [i.food_id for i in ingredients]

    nutrients_by_food = defaultdict(dict)

    for fn in FoodNutrient.objects.filter(
        food_id__in=food_ids, nutrient_id__in=visible_ids
    ).select_related("nutrient"):
        nutrients_by_food[fn.food_id][fn.nutrient_id] = float(fn.amount)

    for ingredient in ingredients:
        ingredient.nutrients = []

        food_values = nutrients_by_food.get(ingredient.food_id, {})

        for nutrient in visible_nutrients:
            amount = food_values.get(nutrient.id, 0) * ingredient.default_servings
            ingredient.nutrients.append(int(amount))

    return {
        "recipe": recipe,
        "form": form,
        "ingredients": ingredients,
        "ingredient_form": RecipeIngredientForm(user=user),
        "visible_nutrients": visible_nutrients,
    }


@login_required
def recipe_edit(request, recipe_id):
    recipe = get_recipe(request.user, recipe_id)

    if request.method == "POST":
        form, response = handle_recipe_edit_post(request, recipe)

        if response:
            return response
    else:
        form = RecipeForm(instance=recipe)

    return render(
        request,
        "recipes/recipe_edit.html",
        get_recipe_context(
            recipe,
            form,
            request.user,
        ),
    )


@login_required
@require_POST
def recipe_delete(request, recipe_id):
    recipe = get_object_or_404(
        Recipe,
        id=recipe_id,
        user=request.user,
    )

    recipe.delete()

    return redirect("recipes")


@login_required
def add_recipe_ingredient(request, recipe_id):
    recipe = get_object_or_404(
        Recipe,
        id=recipe_id,
        user=request.user,
    )

    if request.method == "POST":
        form = RecipeIngredientForm(
            request.POST,
            user=request.user,
        )

        if form.is_valid():
            ingredient = form.save(commit=False)
            ingredient.recipe = recipe
            ingredient.save()

    return redirect("recipe_edit", recipe.id)


@login_required
def ingredient_delete(request, ingredient_id):

    ingredient = get_object_or_404(
        RecipeIngredient,
        id=ingredient_id,
        recipe__user=request.user,
    )
    recipe_id = ingredient.recipe.id

    if request.method == "POST":
        ingredient.delete()

    return redirect("recipe_edit", recipe_id)


@login_required
def recipe_nutrition_ajax(request, recipe_id):
    recipe = get_object_or_404(
        Recipe,
        id=recipe_id,
        user=request.user,
    )

    visible = Nutrient.objects.filter(show_in_recipe=True)

    totals = {nutrient.id: 0 for nutrient in visible}

    for ingredient in recipe.ingredients.all():

        servings = float(
            request.GET.get(
                f"food_{ingredient.food.id}",
                ingredient.default_servings,
            )
        )

        for fn in FoodNutrient.objects.filter(food=ingredient.food):

            if fn.nutrient_id in totals:
                totals[fn.nutrient_id] += float(fn.amount) * servings

    return JsonResponse(totals)


@login_required
def add_recipe_to_diary(request, recipe_id):
    recipe = get_object_or_404(
        Recipe,
        id=recipe_id,
        user=request.user,
    )

    if request.method == "POST":
        form = AddRecipeToDiaryForm(
            request.POST,
            user=request.user,
        )

        if form.is_valid():
            meal = form.cleaned_data["meal"]
            multiplier = form.cleaned_data["portions"]

            for ingredient in recipe.ingredients.all():
                MealFood.objects.create(
                    meal=meal,
                    food=ingredient.food,
                    serving_size=ingredient.food.serving,
                    number_of_servings=(ingredient.default_servings * multiplier),
                )

            return redirect(
                "diary_day",
                date=meal.date,
            )

    else:
        form = AddRecipeToDiaryForm(
            user=request.user,
        )

    return render(
        request,
        "recipes/add_to_diary.html",
        {
            "recipe": recipe,
            "form": form,
        },
    )
