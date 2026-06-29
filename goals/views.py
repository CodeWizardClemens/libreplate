from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import GoalGroup, GoalNutrient, GoalBodyMetric
from nutrients.models import Nutrient
from body_metrics.models import BodyMetric
from .forms import GoalForm


@login_required
def goals_page(request):
    goal_groups = GoalGroup.objects.filter(user=request.user).order_by("-id")

    return render(request, "goals/goals.html", {"goal_groups": goal_groups})


@login_required
def goal_group_create(request):
    if request.method == "POST":
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            form.save_nutrients_and_metrics(goal)

            return redirect("goals")
    else:
        form = GoalForm()

    nutrients = Nutrient.objects.filter(show_in_goal_edit=True)
    body_metrics = BodyMetric.objects.filter(show_in_goal_edit=True)

    return render(
        request,
        "goals/goal_edit.html",
        {
            "form": form,
            "nutrients": nutrients,
            "body_metrics": body_metrics,
            "nutrient_values": {},
            "body_metric_values": {},
        },
    )


@login_required
def goal_group_delete(request, pk):
    group = get_object_or_404(GoalGroup, pk=pk, user=request.user)
    group.delete()
    return redirect("goals")


@login_required
def goal_group_edit(request, pk):
    goal_group = get_object_or_404(GoalGroup, pk=pk, user=request.user)

    if request.method == "POST":
        form = GoalForm(request.POST, instance=goal_group, goal_group=goal_group)

        if form.is_valid():
            goal_group = form.save()
            form.save_nutrients_and_metrics(goal_group)
            return redirect("goals")

    else:
        form = GoalForm(instance=goal_group, goal_group=goal_group)

    nutrient_values = form.get_nutrient_values()
    body_metric_values = form.get_body_metric_values()

    return render(
        request,
        "goals/goal_edit.html",
        {
            "form": form,
            "goal_group": goal_group,
            "nutrients": Nutrient.objects.filter(show_in_goal_edit=True),
            "body_metrics": BodyMetric.objects.filter(show_in_goal_edit=True),
            "nutrient_values": nutrient_values,
            "body_metric_values": body_metric_values,
        },
    )


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
