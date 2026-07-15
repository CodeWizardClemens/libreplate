import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render


@login_required
def settings_page(request):
    return render(
        request,
        "settings/settings.html",
    )

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

