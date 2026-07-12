import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import APIConfigurationForm
from .models import USDAAPISettings


@login_required
def settings_page(request):
    return render(request, "settings/settings.html")


@login_required
def toggle_sidebar(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=400)

    data = json.loads(request.body or "{}")
    collapsed = bool(data.get("collapsed", False))

    user_settings = request.user.settings
    user_settings.collapsed_sidebar = collapsed
    user_settings.save(update_fields=["collapsed_sidebar"])

    return JsonResponse({"success": True, "collapsed": user_settings.collapsed_sidebar})


@login_required
def api_configuration(request):
    # Get the user's settings or create them the first time
    configuration, created = USDAAPISettings.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = APIConfigurationForm(
            request.POST,
            instance=configuration,
        )
        if form.is_valid():
            form.save()
            return redirect("api_configuration")
    else:
        form = APIConfigurationForm(instance=configuration)

    return render(
        request,
        "settings/api_configuration/api_configuration.html",
        {"form": form},
    )
