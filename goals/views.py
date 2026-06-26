from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import GoalGroup, GoalNutrient, GoalBodyMetric
from nutrients.models import Nutrient
from body_metrics.models import BodyMetric
from .forms import GoalGroupForm


@login_required
def goals_page(request):
    groups = GoalGroup.objects.filter(user=request.user).order_by("-id")
    form = GoalGroupForm()

    return render(request, "goals/goals.html", {"groups": groups, "form": form})


@login_required
def add_group(request):
    if request.method == "POST":
        form = GoalGroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.user = request.user
            group.save()

    return redirect("goals")


@login_required
def delete_group(request, pk):
    group = get_object_or_404(GoalGroup, pk=pk, user=request.user)
    group.delete()
    return redirect("goals")


@login_required
def rename_group(request, pk):
    group = get_object_or_404(GoalGroup, pk=pk, user=request.user)

    if request.method == "POST":
        name = request.POST.get("name")
        note = request.POST.get("note")

        if name is not None:
            group.name = name

        if note is not None:
            group.note = note

        group.save()

    return redirect("goals")


@login_required
def add_goal_item(request, pk):
    group = get_object_or_404(GoalGroup, pk=pk, user=request.user)

    nutrients = Nutrient.objects.filter(show_in_diary_total=True)
    body_metrics = BodyMetric.objects.filter(show_in_diary_total=True)

    return render(
        request,
        "goals/add_goal_item.html",
        {"group": group, "nutrients": nutrients, "body_metrics": body_metrics},
    )


@login_required
def add_goal_item_post(request, pk):
    group = get_object_or_404(GoalGroup, pk=pk, user=request.user)

    # 🔥 NUTRIENTS (batch)
    for key, value in request.POST.items():
        if key.startswith("nutrient_") and value:
            nutrient_id = key.replace("nutrient_", "")
            nutrient = Nutrient.objects.get(id=nutrient_id)

            GoalNutrient.objects.create(
                goal_group=group, nutrient=nutrient, amount=value
            )

    # 🔥 BODY METRICS (batch)
    for key, value in request.POST.items():
        if key.startswith("metric_") and value:
            metric_id = key.replace("metric_", "")
            metric = BodyMetric.objects.get(id=metric_id)

            GoalBodyMetric.objects.create(
                goal_group=group, body_metric=metric, amount=value
            )

    return redirect("goals")
