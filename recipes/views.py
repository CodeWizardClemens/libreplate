from django.shortcuts import render, redirect, get_object_or_404

from django.http import JsonResponse

from django.utils import timezone


from nutrients.models import Nutrient

from foods.models import FoodNutrient

from diary.models import MealFood


from .models import Recipe, RecipeIngredient


from .forms import RecipeForm, RecipeIngredientForm, AddRecipeToDiaryForm


def recipe_list(request):

    recipes = Recipe.objects.filter(user=request.user).order_by("name")

    return render(request, "recipes/list.html", {"recipes": recipes})


def recipe_create(request):

    form = RecipeForm(request.POST or None)

    if form.is_valid():

        recipe = form.save(commit=False)

        recipe.user = request.user

        recipe.save()

        return redirect("recipe_edit", recipe.id)

    return render(request, "recipes/create.html", {"form": form})


def recipe_edit(request, recipe_id):

    recipe = get_object_or_404(Recipe, id=recipe_id, user=request.user)

    form = RecipeForm(request.POST or None, instance=recipe)

    if form.is_valid():

        form.save()

        return redirect("recipe_edit", recipe.id)

    ingredient_form = RecipeIngredientForm(user=request.user)

    nutrients = Nutrient.objects.filter(show_in_diary_total=True).order_by("order")

    return render(
        request,
        "recipes/edit.html",
        {
            "recipe": recipe,
            "form": form,
            "ingredients": recipe.ingredients.all(),
            "ingredient_form": ingredient_form,
            "visible_nutrients": nutrients,
        },
    )


def recipe_delete(request, recipe_id):

    recipe = get_object_or_404(Recipe, id=recipe_id, user=request.user)

    if request.method == "POST":

        recipe.delete()

    return redirect("recipes")


def add_recipe_ingredient(request, recipe_id):

    recipe = get_object_or_404(Recipe, id=recipe_id, user=request.user)

    if request.method == "POST":

        form = RecipeIngredientForm(request.POST, user=request.user)

        if form.is_valid():

            ingredient = form.save(commit=False)

            ingredient.recipe = recipe

            ingredient.save()

    return redirect("recipe_edit", recipe.id)


def delete_recipe_ingredient(request, ingredient_id):

    ingredient = get_object_or_404(
        RecipeIngredient, id=ingredient_id, recipe__user=request.user
    )

    recipe_id = ingredient.recipe.id

    if request.method == "POST":

        ingredient.delete()

    return redirect("recipe_edit", recipe_id)


def recipe_nutrition_ajax(request, recipe_id):

    recipe = get_object_or_404(Recipe, id=recipe_id, user=request.user)

    visible = Nutrient.objects.filter(show_in_diary_total=True)

    totals = {}

    for nutrient in visible:

        totals[nutrient.id] = 0

    for ingredient in recipe.ingredients.all():

        servings = float(
            request.GET.get("food_%s" % ingredient.food.id, ingredient.default_servings)
        )

        for fn in FoodNutrient.objects.filter(food=ingredient.food):

            if fn.nutrient_id in totals:

                totals[fn.nutrient_id] += float(fn.amount) * servings

    return JsonResponse(totals)


def add_recipe_to_diary(request, recipe_id):

    recipe = get_object_or_404(Recipe, id=recipe_id, user=request.user)

    if request.method == "POST":

        form = AddRecipeToDiaryForm(request.POST, user=request.user)

        if form.is_valid():

            meal = form.cleaned_data["meal"]

            multiplier = form.cleaned_data["portions"]

            for ingredient in recipe.ingredients.all():

                MealFood.objects.create(
                    meal=meal,
                    food=ingredient.food,
                    serving_size=(ingredient.food.serving),
                    number_of_servings=(ingredient.default_servings * multiplier),
                )

            return redirect("diary_day", date=meal.date)

    else:

        form = AddRecipeToDiaryForm(user=request.user)

    return render(
        request, "recipes/add_to_diary.html", {"recipe": recipe, "form": form}
    )
