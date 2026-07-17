from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import MealPlanForm
from .models import MealPlan, MealPlanFood, MealPlanRecipe, WeekDay

from default_meals.models import DefaultMeal
from foods.models import Food
from recipes.models import Recipe
import logging

logger = logging.getLogger(__name__)


@login_required
def meal_plans(request):
    meal_plans = MealPlan.objects.filter(user=request.user).order_by("-last_used_at")

    return render(
        request,
        "meal_plans/meal_plans.html",
        {
            "meal_plans": meal_plans,
        },
    )


@login_required
def meal_plan_create(request):
    meal_plan = MealPlan.objects.create(
        user=request.user,
    )
    return redirect("meal_plan_edit", meal_plan_id=meal_plan.id)


@login_required
def meal_plan_edit(request, meal_plan_id):
    meal_plan = get_object_or_404(
        MealPlan,
        id=meal_plan_id,
        user=request.user,
    )

    if request.method == "POST":
        form = MealPlanForm(request.POST, instance=meal_plan)
        if form.is_valid():
            form.save()
            return redirect("meal_plans")
    else:
        form = MealPlanForm(instance=meal_plan)

    default_meals = DefaultMeal.objects.filter(user=request.user)

    # Group existing entries by "meal_id-day" string keys
    cell_contents = {}

    food_entries = MealPlanFood.objects.filter(
        meal_plan=meal_plan
    ).select_related("food", "meal")
    for entry in food_entries:
        key = f"{entry.meal_id}-{entry.day}"
        cell_contents.setdefault(key, []).append({
            "name": entry.food.name,
            "type": "food",
            "id": entry.id,
        })

    recipe_entries = MealPlanRecipe.objects.filter(
        meal_plan=meal_plan
    ).select_related("recipe", "meal")
    for entry in recipe_entries:
        key = f"{entry.meal_id}-{entry.day}"
        cell_contents.setdefault(key, []).append({
            "name": entry.recipe.name,
            "type": "recipe",
            "id": entry.id,
        })

    return render(
        request,
        "meal_plans/meal_plan_edit.html",
        {
            "form": form,
            "meal_plan": meal_plan,
            "default_meals": default_meals,
            "cell_contents": cell_contents,
        },
    )


@login_required
def meal_plan_copy(request, meal_plan_id):
    meal_plan = get_object_or_404(
        MealPlan,
        id=meal_plan_id,
        user=request.user,
    )

    MealPlan.objects.create(
        user=request.user,
        name=f"{meal_plan.name} (Copy)",
        description=meal_plan.description,
    )

    return redirect("meal_plans")


@login_required
def meal_plan_delete(request, meal_plan_id):
    meal_plan = get_object_or_404(
        MealPlan,
        id=meal_plan_id,
        user=request.user,
    )

    if request.method == "POST":
        meal_plan.delete()
        return HttpResponse(status=200)

    return HttpResponse(status=405)


@login_required
def meal_plan_title(request, pk):
    meal_plan = get_object_or_404(
        MealPlan,
        pk=pk,
        user=request.user,
    )

    return render(
        request,
        "meal_plans/partials/title.html",
        {
            "meal_plan": meal_plan,
        },
    )


@login_required
def meal_plan_rename_form(request, pk):
    meal_plan = get_object_or_404(
        MealPlan,
        pk=pk,
        user=request.user,
    )

    return render(
        request,
        "meal_plans/partials/title_form.html",
        {
            "meal_plan": meal_plan,
        },
    )


@login_required
def meal_plan_rename(request, pk):
    meal_plan = get_object_or_404(
        MealPlan,
        pk=pk,
        user=request.user,
    )

    if request.method == "POST":
        name = request.POST.get("name", "").strip()

        if name:
            meal_plan.name = name
        else:
            meal_plan.name = MealPlan._meta.get_field("name").default
        meal_plan.save()

    return render(
        request,
        "meal_plans/partials/title.html",
        {
            "meal_plan": meal_plan,
        },
    )


@login_required
def cell_menu(request, meal_plan_id, meal_id, day):
    """Returns a Bootstrap modal partial with a dropdown of all foods & recipes."""
    meal_plan = get_object_or_404(MealPlan, id=meal_plan_id, user=request.user)
    meal = get_object_or_404(DefaultMeal, id=meal_id, user=request.user)

    foods = Food.objects.filter(user=request.user).order_by("name")
    recipes = Recipe.objects.filter(user=request.user).order_by("name")

    logger.info(f"User '{request.user}' opened cell menu for meal '{meal}' on '{WeekDay(int(day)).label}'.")

    return render(
        request,
        "meal_plans/partials/cell_menu.html",
        {
            "meal_plan": meal_plan,
            "meal": meal,
            "day": int(day),
            "day_display": WeekDay(int(day)).label,
            "foods": foods,
            "recipes": recipes,
        },
    )


def _render_cell(request, meal_plan, meal_id, day):
    """Re-fetch items for a cell and return the rendered partial."""
    food_entries = MealPlanFood.objects.filter(
        meal_plan=meal_plan, meal_id=meal_id, day=int(day)
    ).select_related("food")
    recipe_entries = MealPlanRecipe.objects.filter(
        meal_plan=meal_plan, meal_id=meal_id, day=int(day)
    ).select_related("recipe")

    cell_items = [
        {"name": e.food.name, "type": "food", "id": e.id}
        for e in food_entries
    ] + [
        {"name": e.recipe.name, "type": "recipe", "id": e.id}
        for e in recipe_entries
    ]

    return render(
        request,
        "meal_plans/partials/cell_content.html",
        {
            "cell_items": cell_items,
            "meal_plan": meal_plan,
            "meal_id": meal_id,
            "day": day,
        },
    )


@login_required
def cell_remove_food(request, meal_plan_id, meal_plan_food_id):
    """Delete a MealPlanFood entry and return updated cell."""
    meal_plan = get_object_or_404(MealPlan, id=meal_plan_id, user=request.user)

    meal_id = request.POST.get("meal_id")
    day = request.POST.get("day")

    entry = MealPlanFood.objects.filter(
        id=meal_plan_food_id,
        meal_plan=meal_plan,
    ).first()
    
    if entry:
        entry.delete()

    return _render_cell(request, meal_plan, meal_id, day)


@login_required
def cell_remove_recipe(request, meal_plan_id, meal_plan_recipe_id):
    """Delete a MealPlanRecipe entry and return updated cell."""
    meal_plan = get_object_or_404(MealPlan, id=meal_plan_id, user=request.user)

    meal_id = request.POST.get("meal_id")
    day = request.POST.get("day")

    entry = MealPlanRecipe.objects.filter(
        id=meal_plan_recipe_id,
        meal_plan=meal_plan,
    ).first()
    
    if entry:
        entry.delete()

    return _render_cell(request, meal_plan, meal_id, day)


@login_required
def cell_add_item(request, meal_plan_id):
    """Handles the POST from the modal: adds a food or recipe to the cell."""

    meal_plan = get_object_or_404(MealPlan, id=meal_plan_id, user=request.user)

    if request.method != "POST":
        return HttpResponse(status=405)

    item_type = request.POST.get("item_type")  # "food" or "recipe"
    item_id = request.POST.get("item_id")
    meal_id = request.POST.get("meal_id")
    day = request.POST.get("day")

    meal = get_object_or_404(DefaultMeal, id=meal_id, user=request.user)

    try:
        if item_type == "food":
            food = get_object_or_404(Food, id=item_id, user=request.user)
            MealPlanFood.objects.create(
                meal_plan=meal_plan,
                meal=meal,
                food=food,
                day=int(day),
                serving_size=food.serving,
                number_of_servings=1,
            )

        elif item_type == "recipe":
            recipe = get_object_or_404(Recipe, id=item_id, user=request.user)
            MealPlanRecipe.objects.create(
                meal_plan=meal_plan,
                meal=meal,
                recipe=recipe,
                day=int(day),
                serving_size=1,
                number_of_servings=1,
            )
        else:
            return HttpResponse("Invalid item type", status=400)
    except Exception as e:
        logger.exception(f"Error adding item: {e}")
        return HttpResponse(f"Error: {str(e)}", status=400)

    return _render_cell(request, meal_plan, meal_id, day)