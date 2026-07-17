from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import MealPlanForm
from .models import MealPlan

from default_meals.models import DefaultMeal

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

    return render(
        request,
        "meal_plans/meal_plan_edit.html",
        {
            "form": form,
            "meal_plan": meal_plan,
            "default_meals": DefaultMeal.objects.filter(user=request.user),
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
    if request.method != "POST":
        return HttpResponse(status=405)

    return render(
        request,
        "meal_plans/partials/title.html",
        {
            "meal_plan": meal_plan,
        },
    )
