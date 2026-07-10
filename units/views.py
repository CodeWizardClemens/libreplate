from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import UnitForm
from .models import Unit


@login_required
def units(request):
    units = Unit.objects.order_by("name")
    context = {"units": units}
    return render(request, "units/units.html", context)


@login_required
def create_unit(request):
    if request.method == "POST":
        form = UnitForm(request.POST, scope=request.user.unit_scope)
        if form.is_valid():
            unit = form.save(commit=False)
            unit.user = request.user  # Assign the current user
            unit.save()
            return redirect("units")
    else:
        form = UnitForm(None, scope=request.user.unit_scope)
    return render(request, "units/unit_form.html", {"form": form})


@login_required
def edit_unit(request, pk):
    unit = get_object_or_404(Unit, pk=pk)

    # Security check: Only allow editing if it belongs to this user OR it's a global unit
    # (Decide policy: Can users edit global units? Usually no. Let's restrict to user-owned
    # or admin)
    if unit.user and unit.user != request.user:
        return redirect("units")  # Or raise PermissionDenied

    if request.method == "POST":
        form = UnitForm(request.POST, instance=unit, scope=request.user.unit_scope)
        if form.is_valid():
            form.save()
            return redirect("units")
    else:
        form = UnitForm(instance=unit, scope=request.user.unit_scope)

    return render(request, "units/unit_form.html", {"form": form})


@login_required
def delete_unit(request, pk):
    unit = get_object_or_404(Unit, pk=pk)

    # Security check: Only allow deletion of owned units (or global if you want)
    if unit.user and unit.user != request.user:
        return redirect("units")

    if request.method == "POST":
        unit.delete()
        return redirect("units")

    return render(request, "units/unit_confirm_delete.html", {"unit": unit})
