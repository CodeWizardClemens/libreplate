from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@login_required
def toggle_dark_mode(request):
    preferences = request.user.preferences

    preferences.dark_mode = not preferences.dark_mode
    preferences.save()

    return redirect(request.META.get("HTTP_REFERER", "/"))


@login_required
def update_theme_color(request):
    if request.method == "POST":
        color = request.POST.get("theme_color")

        if color:
            request.user.preferences.theme_color = color
            request.user.preferences.save()

    return JsonResponse({"status": "ok"})


@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(
        request,
        username=username,
        password=password,
    )

    if user is None:
        return Response(
            {"error": "Invalid credentials"},
            status=400,
        )

    login(request, user)

    return Response(
        {
            "message": "Logged in",
            "username": user.username,
        }
    )


@api_view(["POST"])
def logout_view(request):
    logout(request)

    return Response(
        {"message": "Logged out"}
    )