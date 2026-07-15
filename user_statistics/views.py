from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from body_metrics.models import BodyMetric
from nutrients.models import Nutrient

from .forms import GraphForm
from .models import Graph, GraphLine, GraphLineBodyMetric, GraphLineNutrient

from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta

from django.db.models import Sum, F
from django.db.models.functions import TruncDate
from django.http import JsonResponse
from django.utils import timezone

from body_metrics.models import BodyMetricLog
# TODO move MealFood to a meal app, allong with default meals.
from diary.models import MealFood

@login_required
def graph_data(request, pk):

    graph = get_object_or_404(
        Graph.objects.prefetch_related(
            "lines",
            "lines__body_metric__body_metric",
            "lines__nutrient__nutrient",
        ),
        pk=pk,
        user=request.user,
    )

    start, end = get_graph_date_range(graph)

    datasets = []

    labels = set()

    for line in graph.lines.all():

        #
        # BODY METRIC
        #

        if hasattr(line, "body_metric"):

            qs = BodyMetricLog.objects.filter(
                user=request.user,
                body_metric=line.body_metric.body_metric,
            )

            if start:
                qs = qs.filter(date__gte=start)

            qs = qs.filter(date__lte=end).order_by("date")

            values = {}

            for log in qs:
                values[str(log.date)] = log.amount
                labels.add(str(log.date))

            datasets.append(
                {
                    "label": line.name,
                    "values": values,
                }
            )

        #
        # NUTRIENT
        #

        else:

            nutrient = line.nutrient.nutrient

            qs = (
                MealFood.objects.filter(
                    meal__user=request.user,
                    food__food_nutrients__nutrient=nutrient,
                )
                .annotate(day=TruncDate("meal__date"))
                .values("day")
                .annotate(
                    total=Sum(
                        F("food__food_nutrients__amount")
                        * F("serving_size")
                        * F("number_of_servings")
                        / F("food__serving")
                    )
                )
                .order_by("day")
            )

            if start:
                qs = qs.filter(day__gte=start)

            qs = qs.filter(day__lte=end)

            values = {}

            for row in qs:
                values[str(row["day"])] = float(row["total"])
                labels.add(str(row["day"]))

            datasets.append(
                {
                    "label": line.name,
                    "values": values,
                }
            )

    labels = sorted(labels)

    chart_data = []

    for ds in datasets:

        chart_data.append(
            {
                "label": ds["label"],
                "data": [
                    ds["values"].get(label)
                    for label in labels
                ],
            }
        )

    return JsonResponse(
        {
            "labels": labels,
            "datasets": chart_data,
            "type": graph.graph_type,
        }
    )

def get_graph_date_range(graph):
    if graph.period_end_mode == Graph.PeriodEndMode.NOW:
        end = timezone.now().date()

    elif graph.period_end_mode == Graph.PeriodEndMode.CUSTOM:
        end = graph.period_end_date.date()

    else:
        latest = None

        for line in graph.lines.all():

            if hasattr(line, "body_metric"):

                d = (
                    BodyMetricLog.objects.filter(
                        user=graph.user,
                        body_metric=line.body_metric.body_metric,
                    )
                    .order_by("-date")
                    .first()
                )

                if d:
                    latest = max(latest, d.date) if latest else d.date

            elif hasattr(line, "nutrient"):

                d = (
                    MealFood.objects.filter(
                        meal__user=graph.user,
                        food__food_nutrients__nutrient=line.nutrient.nutrient,
                    )
                    .order_by("-meal__date")
                    .first()
                )

                if d:
                    latest = max(latest, d.meal.date) if latest else d.meal.date

        end = latest or timezone.now().date()

    if graph.period_unit == Graph.PeriodUnit.ALL:
        return None, end

    amount = graph.period_amount

    if graph.period_unit == Graph.PeriodUnit.DAY:
        start = end - timedelta(days=amount)

    elif graph.period_unit == Graph.PeriodUnit.WEEK:
        start = end - timedelta(days=amount * 7)

    elif graph.period_unit == Graph.PeriodUnit.MONTH:
        start = end - timedelta(days=amount * 30)

    else:
        start = end - timedelta(days=amount * 365)

    return start, end

def get_graph_line_choices():
    return [
        (
            "Body Metrics",
            [
                (f"body_metric:{metric.pk}", metric.name)
                for metric in BodyMetric.objects.order_by("name")
            ],
        ),
        (
            "Nutrients",
            [
                (f"nutrient:{nutrient.pk}", nutrient.name)
                for nutrient in Nutrient.objects.order_by("name")
            ],
        ),
    ]


def get_line_selected_value(line):
    if hasattr(line, "body_metric"):
        return f"body_metric:{line.body_metric.body_metric_id}"

    if hasattr(line, "nutrient"):
        return f"nutrient:{line.nutrient.nutrient_id}"

    return ""


def create_graph_lines(graph, request):
    choices = request.POST.getlist("line_choice")
    names = request.POST.getlist("line_name")
    units = request.POST.getlist("moving_average_unit")
    amounts = request.POST.getlist("moving_average_amount")

    for choice, custom_name, unit, amount in zip(
        choices, names, units, amounts
    ):
        if not choice:
            continue

        line = GraphLine.objects.create(
            graph=graph,
            name=custom_name or "",
            moving_average_unit=unit or None,
            moving_average_amount=amount or 1,
        )

        model, pk = choice.split(":")

        if model == "body_metric":
            metric = get_object_or_404(BodyMetric, pk=pk)

            if not line.name:
                line.name = metric.name
                line.save()

            GraphLineBodyMetric.objects.create(
                graph_line=line,
                body_metric=metric,
            )

        elif model == "nutrient":
            nutrient = get_object_or_404(Nutrient, pk=pk)

            if not line.name:
                line.name = nutrient.name
                line.save()

            GraphLineNutrient.objects.create(
                graph_line=line,
                nutrient=nutrient,
            )


@login_required
def graph_list(request):
    graphs = Graph.objects.filter(user=request.user)

    return render(
        request,
        "user_statistics/graph_list.html",
        {"graphs": graphs},
    )


@login_required
def graph_create(request):
    if request.method == "POST":
        form = GraphForm(request.POST)

        if form.is_valid():
            graph = form.save(commit=False)
            graph.user = request.user
            graph.save()

            create_graph_lines(graph, request)

            return redirect("graph_list")
    else:
        form = GraphForm()

    return render(
        request,
        "user_statistics/graph_form.html",
        {
            "graph": None,
            "lines": [],
            "form": form,
            "line_choices": get_graph_line_choices(),
        },
    )


@login_required
def graph_edit(request, pk):
    graph = get_object_or_404(Graph, pk=pk, user=request.user)

    if request.method == "POST":
        form = GraphForm(request.POST, instance=graph)

        if form.is_valid():
            form.save()
            graph.lines.all().delete()
            create_graph_lines(graph, request)

            return redirect("graph_list")
    else:
        form = GraphForm(instance=graph)

    lines = list(
        graph.lines.select_related(
            "body_metric__body_metric",
            "nutrient__nutrient",
        )
    )

    for line in lines:
        line.selected_value = get_line_selected_value(line)

    return render(
        request,
        "user_statistics/graph_form.html",
        {
            "graph": graph,
            "lines": lines,
            "form": form,
            "line_choices": get_graph_line_choices(),
        },
    )


@login_required
def graph_delete(request, pk):
    graph = get_object_or_404(Graph, pk=pk, user=request.user)
    graph.delete()
    return HttpResponse("")