from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .forms import UnitForm
from .models import Unit, UnitScope


@login_required
def units(request):
    global_scope = UnitScope.objects.get(user=None)
    user_scope = request.user.unit_scope
    context = {
        "units_global": Unit.objects.filter(scope=global_scope),
        "units_user": Unit.objects.filter(scope=user_scope),
        "page_title": "Units",
    }
    return render(
        request,
        "units/units.html",
        context
    )


@login_required
def unit_form(request, pk=None):
    if pk:
        unit = get_object_or_404(Unit, pk=pk, scope=request.user.unit_scope)
    else:
        # New unit
        unit = None

    if request.method == "POST":
        form = UnitForm(
            request.POST,
            instance=unit,
            scope=request.user.unit_scope,
        )
        if form.is_valid():
            unit = form.save(commit=False)
            # No PK means the unit is not saved to the db yet.
            if unit.pk is None:
                unit.scope = request.user.unit_scope
            unit.save()

            return redirect("units")
    else:
        form = UnitForm(
            instance=unit,
            scope=request.user.unit_scope,
        )
    return render(
        request, "units/unit_form.html",
        {
            "form": form,
            "unit": unit,
            "page_title": "Create unit",
        }
    )


@require_POST
@login_required
def unit_delete(request, pk):
    scope = request.user.unit_scope
    unit = get_object_or_404(Unit, pk=pk, scope=scope)
    unit.delete()
    return redirect("units")
