from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ScriptForm
from .lua_runner import execute_script
from .models import Script


@login_required
def scripts(request):
    scripts = Script.objects.filter(user=request.user)

    return render(
        request,
        "scripts/scripts.html",
        {
            "scripts": scripts,
        },
    )


@login_required
def delete_script(request, script_id):
    if request.method != "POST":
        return redirect("scripts")

    script = get_object_or_404(
        Script,
        id=script_id,
        user=request.user,
    )

    script.delete()
    return redirect("scripts")


@login_required
def script_create(request):
    if request.method == "POST":
        form = ScriptForm(request.POST)

        if form.is_valid():
            script = form.save(commit=False)
            script.user = request.user
            script.lua_version = "LuaJIT"
            script.save()

            return redirect("edit_script", script.id)

    else:
        form = ScriptForm()

    return render(
        request,
        "scripts/script_edit.html",
        {
            "form": form,
        },
    )


@login_required
def edit_script(request, script_id):
    script = get_object_or_404(
        Script,
        id=script_id,
        user=request.user,
    )

    if request.method == "POST":
        form = ScriptForm(
            request.POST,
            instance=script,
        )

        if form.is_valid():
            form.save()

            return redirect("edit_script", script.id)

    else:
        form = ScriptForm(instance=script)

    return render(
        request,
        "scripts/script_edit.html",
        {
            "script": script,
            "form": form,
        },
    )


@login_required
def run_script(request, script_id):
    script = get_object_or_404(
        Script,
        id=script_id,
        user=request.user,
    )

    result = execute_script(script)

    if result["redirect"]:
        return redirect(result["redirect"])

    return redirect("scripts")