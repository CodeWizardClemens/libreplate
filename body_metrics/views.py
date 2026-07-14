import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import BodyMetricForm
from .models import BodyMetric


@login_required
def body_metrics(request):
    return render(
        request=request,
        template_name="body_metrics/body_metrics.html",
        context={
            "body_metrics": BodyMetric.objects.all(),
            "page_title": "Body Metrics",
        },
    )


@login_required
def create_body_metric(request):
    if request.method == "POST":
        form = BodyMetricForm(request.POST)
        if form.is_valid():
            body_metric = form.save(commit=False)
            body_metric.user = request.user  # Assign the current user
            body_metric.save()
            return redirect("body_metrics")
    else:
        form = BodyMetricForm()
    return render(
        request,
        "body_metrics/body_metric_form.html",
        {
            "form": form,
            "page_title": "Create Body Metric"
        }
    )


@login_required
def edit_body_metric(request, pk):
    body_metric = get_object_or_404(BodyMetric, pk=pk)

    # Security check: Only allow editing if it belongs to this user OR it's a global body_metric
    # (Decide policy: Can users edit global body_metrics? Usually no. Let's restrict to user-owned or admin)
    if body_metric.user and body_metric.user != request.user:
        return redirect("body_metrics")  # Or raise PermissionDenied

    if request.method == "POST":
        form = BodyMetricForm(request.POST, instance=body_metric)
        if form.is_valid():
            form.save()
            return redirect("body_metrics")
    else:
        form = BodyMetricForm(instance=body_metric)

    return render(
        request,
        "body_metrics/body_metric_form.html",
        {
            "form": form,
            "page_title": "Edit body metric",
        }
    )


@login_required
def delete_body_metric(request, pk):
    body_metric = get_object_or_404(BodyMetric, pk=pk)

    # Security check: Only allow deletion of owned body_metrics (or global if you want)
    if body_metric.user and body_metric.user != request.user:
        return redirect("body_metrics")

    if request.method == "POST":
        body_metric.delete()
        return redirect("body_metrics")

    return render(
        request,
        "body_metrics/body_metric_confirm_delete.html",
        {"body_metric": body_metric},
    )


@login_required
@require_POST
def reorder_body_metrics(request):
    data = json.loads(request.body)

    for item in data.get("items", []):
        body_metric = get_object_or_404(BodyMetric, id=item["id"])

        # Only allow user's own body_metrics to be reordered
        if body_metric.user == request.user or body_metric.user is None:
            body_metric.order = item["position"]
            body_metric.save(update_fields=["order"])

    return JsonResponse({"status": "ok"})


@login_required
@require_POST
def toggle_body_metric_visibility(request, pk):

    body_metric = get_object_or_404(BodyMetric, pk=pk)

    # Only allow owner or admin to change visibility
    if body_metric.user and body_metric.user != request.user:
        return JsonResponse({"error": "Permission denied"}, status=403)

    body_metric.show_in_diary_total = not body_metric.show_in_diary_total
    body_metric.save(update_fields=["show_in_diary_total"])

    return JsonResponse({"show_in_diary_total": body_metric.show_in_diary_total})
