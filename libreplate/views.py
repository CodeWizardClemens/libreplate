# libreplate/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


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
def default_page(request):
    return redirect("diary_today")
