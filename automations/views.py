from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AutomationForm
from .lua_runner import execute_automation
from .models import Automation


@login_required
def automations(request):
    automations = Automation.objects.filter(user=request.user)

    return render(
        request,
        "automations/automations.html",
        {
            "automations": automations,
        },
    )


@login_required
def delete_automation(request, automation_id):
    if request.method != "POST":
        return redirect("automations")

    automation = get_object_or_404(
        Automation,
        id=automation_id,
        user=request.user,
    )

    automation.delete()
    return redirect("automations")


@login_required
def automation_create(request):
    if request.method == "POST":
        form = AutomationForm(request.POST)

        if form.is_valid():
            automation = form.save(commit=False)
            automation.user = request.user
            automation.lua_version = "LuaJIT"
            automation.save()

            return redirect("edit_automation", automation.id)

    else:
        form = AutomationForm()

    return render(
        request,
        "automations/automation_edit.html",
        {
            "form": form,
        },
    )


@login_required
def edit_automation(request, automation_id):
    automation = get_object_or_404(
        Automation,
        id=automation_id,
        user=request.user,
    )

    if request.method == "POST":
        form = AutomationForm(
            request.POST,
            instance=automation,
        )

        if form.is_valid():
            form.save()

            return redirect("edit_automation", automation.id)

    else:
        form = AutomationForm(instance=automation)

    return render(
        request,
        "automations/automation_edit.html",
        {
            "automation": automation,
            "form": form,
        },
    )


@login_required
def run_automation(request, automation_id):
    automation = get_object_or_404(
        Automation,
        id=automation_id,
        user=request.user,
    )

    result = execute_automation(automation)

    if result["redirect"]:
        return redirect(result["redirect"])

    return redirect("automations")
