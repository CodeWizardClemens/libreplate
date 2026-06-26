# libreplate/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def profile(request):
    return render(
        request,
        "profile.html",
        {
            "user": request.user,
        },
    )


@login_required
def units(request):
    return render(request, "units.html")


@login_required
def nutrients(request):
    return render(request, "nutrients.html")


@login_required
def foods(request):
    return render(request, "foods.html")


@login_required
def diary(request):
    return render(request, "day.html")


@login_required
def goals_page(request):
    return render(request, "goals_page.html")
