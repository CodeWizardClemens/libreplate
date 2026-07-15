import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import NutrientForm
from .models import Nutrient


@login_required
def nutrients(request):
    nutrients = Nutrient.objects.all()
    return render(
        request,
        "nutrients/nutrients.html",
        {
            "nutrients": nutrients,
        }
    )


@login_required
def create_nutrient(request):
    if request.method == "POST":
        form = NutrientForm(request.POST)
        if form.is_valid():
            nutrient = form.save(commit=False)
            nutrient.user = request.user  # Assign the current user
            nutrient.save()
            return redirect("nutrients")
    else:
        form = NutrientForm()
    return render(
        request,
        "nutrients/nutrient_form.html",
        {
            "form": form,
        }
    )


@login_required
def edit_nutrient(request, pk):
    nutrient = get_object_or_404(Nutrient, pk=pk)

    if request.method == "POST":
        form = NutrientForm(request.POST, instance=nutrient)
        if form.is_valid():
            form.save()
            return redirect("nutrients")
    else:
        form = NutrientForm(instance=nutrient)

    return render(
        request,
        "nutrients/nutrient_form.html",
        {
            "form": form,
        }
    )


@login_required
def delete_nutrient(request, pk):
    nutrient = get_object_or_404(Nutrient, pk=pk)

    # Security check: Only allow deletion of owned nutrients (or global if you want)
    if nutrient.user and nutrient.user != request.user:
        return redirect("nutrients")

    if request.method == "POST":
        nutrient.delete()
        return redirect("nutrients")

    return render(
        request, "nutrients/nutrient_confirm_delete.html", {"nutrient": nutrient}
    )


@login_required
@require_POST
def reorder_nutrients(request):
    data = json.loads(request.body)

    for item in data.get("items", []):
        nutrient = get_object_or_404(Nutrient, id=item["id"])

        # Only allow user's own nutrients to be reordered
        if nutrient.user == request.user or nutrient.user is None:
            nutrient.order = item["position"]
            nutrient.save(update_fields=["order"])

    return JsonResponse({"status": "ok"})
