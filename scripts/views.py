from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from foods.models import Food

from .executors import EXECUTORS
from .forms import ScriptForm
from .functions import SCRIPT_FUNCTIONS
from .models import Script, ScriptStep


@login_required
def scripts(request):

    scripts = Script.objects.filter(user=request.user)

    return render(request, "scripts/scripts.html", {"scripts": scripts})


@login_required
def script_create(request):

    if request.method == "POST":
        form = ScriptForm(request.POST)

        if form.is_valid():
            script = form.save(commit=False)
            script.user = request.user
            script.save()
            return redirect("edit_script", script.id)

    else:
        form = ScriptForm()

    return render(request, "scripts/script_create.html", {"form": form})


@login_required
def edit_script(request, script_id):

    script = get_object_or_404(Script, id=script_id, user=request.user)

    if request.method == "POST":
        script.name = request.POST.get("name")
        script.description = request.POST.get("description")
        script.save()

    return render(
        request,
        "scripts/script_edit.html",
        {"script": script, "functions": SCRIPT_FUNCTIONS},
    )


@login_required
def add_step(request, script_id):

    script = get_object_or_404(Script, id=script_id, user=request.user)

    function_key = request.POST.get("function_key")

    ScriptStep.objects.create(
        script=script, function_key=function_key, order=script.steps.count(), config={}
    )

    return redirect("edit_script", script.id)


@login_required
def update_step(request, step_id):

    step = get_object_or_404(ScriptStep, id=step_id, script__user=request.user)

    if request.method == "POST":

        func = SCRIPT_FUNCTIONS.get(step.function_key, {})

        new_config = {}

        for field in func.get("fields", []):

            value = request.POST.get(field["name"])

            if field["type"] == "integer":
                try:
                    value = int(value)
                except:
                    value = 0

            new_config[field["name"]] = value

        step.config = new_config
        step.save()

    return redirect("edit_script", step.script.id)


@login_required
def delete_step(request, step_id):

    step = get_object_or_404(ScriptStep, id=step_id, script__user=request.user)

    script_id = step.script.id
    step.delete()

    return redirect("edit_script", script_id)


@login_required
def run_script(request, script_id):

    script = get_object_or_404(Script, id=script_id, user=request.user)

    for step in script.steps.all():

        executor = EXECUTORS.get(step.function_key)

        if executor:
            executor(request.user, step.config)

    return redirect("scripts")


@login_required
def select_food_for_step(request, step_id, food_id):
    step = get_object_or_404(ScriptStep, id=step_id, script__user=request.user)
    food = get_object_or_404(Food, id=food_id, user=request.user)

    config = step.config or {}
    config["food_id"] = food.id
    step.config = config
    step.save()

    return redirect("edit_script", step.script.id)
