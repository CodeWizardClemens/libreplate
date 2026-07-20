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
def appearance(request):
    return render(
        request,
        "settings/appearance.html",
    )
