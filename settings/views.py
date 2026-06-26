import json

from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import DefaultMeal
from .forms import DefaultMealForm
from django.shortcuts import render, get_object_or_404, redirect


@login_required
def settings_page(request):
    return render(request, "settings/settings.html")


@login_required
def toggle_sidebar(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=400)

    data = json.loads(request.body or "{}")
    collapsed = bool(data.get("collapsed", False))

    user_settings = request.user.settings
    user_settings.collapsed_sidebar = collapsed
    user_settings.save(update_fields=["collapsed_sidebar"])

    return JsonResponse({"success": True, "collapsed": user_settings.collapsed_sidebar})


##########################


@login_required
def default_meals(request):
    default_meals = DefaultMeal.objects.all()
    context = {"default_meals": default_meals}
    return render(request, "settings/default_meals/default_meals.html", context)


@login_required
def create_default_meal(request):
    if request.method == "POST":
        form = DefaultMealForm(request.POST)
        if form.is_valid():
            default_meal = form.save(commit=False)
            default_meal.user = request.user  # Assign the current user
            default_meal.save()
            return redirect("default_meals")
    else:
        form = DefaultMealForm()
    return render(
        request, "settings/default_meals/default_meal_form.html", {"form": form}
    )


@login_required
def edit_default_meal(request, pk):
    default_meal = get_object_or_404(DefaultMeal, pk=pk)

    # Security check: Only allow editing if it belongs to this user OR it's a global default_meal
    # (Decide policy: Can users edit global default_meals? Usually no. Let's restrict to user-owned or admin)
    if default_meal.user and default_meal.user != request.user:
        return redirect("default_meals")  # Or raise PermissionDenied

    if request.method == "POST":
        form = DefaultMealForm(request.POST, instance=default_meal)
        if form.is_valid():
            form.save()
            return redirect("default_meals")
    else:
        form = DefaultMealForm(instance=default_meal)

    return render(
        request, "settings/default_meals/default_meal_form.html", {"form": form}
    )


@login_required
def delete_default_meal(request, pk):
    default_meal = get_object_or_404(DefaultMeal, pk=pk)

    # Security check: Only allow deletion of owned default_meals (or global if you want)
    if default_meal.user and default_meal.user != request.user:
        return redirect("default_meals")

    if request.method == "POST":
        default_meal.delete()
        return redirect("default_meals")

    return render(
        request,
        "settings/default_meals/default_meal_confirm_delete.html",
        {"default_meal": default_meal},
    )


@login_required
@require_POST
def reorder_default_meals(request):
    data = json.loads(request.body)

    for item in data.get("items", []):
        default_meal = get_object_or_404(DefaultMeal, id=item["id"])

        # Only allow user's own default_meals to be reordered
        if default_meal.user == request.user or default_meal.user is None:
            default_meal.order = item["position"]
            default_meal.save(update_fields=["order"])

    return JsonResponse({"status": "ok"})
