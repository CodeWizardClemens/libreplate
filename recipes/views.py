from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse

from nutrients.models import Nutrient
from foods.models import FoodNutrient
from diary.models import MealFood

from .models import Recipe, RecipeIngredient
from .forms import (
    RecipeForm,
    RecipeIngredientForm,
    AddRecipeToDiaryForm,
)
from collections import defaultdict
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.utils import timezone

def selected_recipes(user, ids):
    return Recipe.objects.filter(
        user=user,
        id__in=ids,
    ).prefetch_related("ingredients__food")

@login_required
def recipes(request):

    meal_id = request.GET.get("meal")
    meal_name = request.GET.get("meal_name")

    recipes = Recipe.objects.filter(user=request.user).order_by("name")

    return render(
        request,
        "recipes/recipes.html",
        {
            "recipes": recipes,
            "meal_id": meal_id,
            "meal_name": meal_name,
        },
    )

@login_required
def add_recipes_to_meal_direct(request, meal_id):
    if request.method != "POST":
        return redirect("recipes")

    from diary.views import get_or_create_real_meal

    meal = get_or_create_real_meal(
        meal_id,
        request.user,
        date=timezone.localdate(),
    )

    recipes = (
        Recipe.objects.filter(
            user=request.user,
            id__in=request.POST.getlist("recipes"),
        )
        .prefetch_related("ingredients__food")
    )

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
            notes.append(
                f"Description: {recipe.summary}"
            )            
        if recipe.instructions:
            notes.append(
                f"\n{recipe.instructions.strip()}"
            )

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


@login_required
def recipe_edit(request, recipe_id):
    recipe = get_object_or_404(
        Recipe,
        id=recipe_id,
        user=request.user,
    )

    if request.method == "POST":
        form = RecipeForm(request.POST, instance=recipe)

        if form.is_valid():
            form.save()

            # Save ingredient values
            for ingredient in recipe.ingredients.all():

                serving_amount = request.POST.get(
                    f"serving_amount_{ingredient.id}"
                )

                default_servings = request.POST.get(
                    f"default_servings_{ingredient.id}"
                )

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

            return redirect("recipes")

    else:
        form = RecipeForm(instance=recipe)

    ingredient_form = RecipeIngredientForm(user=request.user)

    visible_nutrients = (
        Nutrient.objects.filter(show_in_recipe=True)
        .order_by("order")
    )

    recipe_totals = defaultdict(float)

    for ingredient in recipe.ingredients.all():

        nutrient_values = defaultdict(float)

        for fn in ingredient.food.food_nutrients.all():

            amount = float(fn.amount) * ingredient.default_servings

            nutrient_values[fn.nutrient_id] = amount
            recipe_totals[fn.nutrient_id] += amount

        ingredient.nutrient_values = {
            k: int(v)
            for k, v in nutrient_values.items()
        }

    recipe.total_nutrients = {
        k: int(v)
        for k, v in recipe_totals.items()
    }

    return render(
        request,
        "recipes/recipe_edit.html",
        {
            "recipe": recipe,
            "form": form,
            "ingredients": recipe.ingredients.all(),
            "ingredient_form": ingredient_form,
            "visible_nutrients": visible_nutrients,
        },
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

    totals = {
        nutrient.id: 0
        for nutrient in visible
    }

    for ingredient in recipe.ingredients.all():

        servings = float(
            request.GET.get(
                f"food_{ingredient.food.id}",
                ingredient.default_servings,
            )
        )

        for fn in FoodNutrient.objects.filter(food=ingredient.food):

            if fn.nutrient_id in totals:
                totals[fn.nutrient_id] += (
                    float(fn.amount) * servings
                )

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
                    number_of_servings=(
                        ingredient.default_servings * multiplier
                    ),
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