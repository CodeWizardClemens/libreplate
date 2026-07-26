from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token

from rest_framework.decorators import (
    api_view,
    permission_classes,
)

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)

from rest_framework.response import Response
from rest_framework import status


@api_view(["GET"])
@permission_classes([AllowAny])
def csrf_view(request):
    return Response(
        {
            "csrfToken": get_token(request),
        }
    )


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
            {
                "detail": "Invalid credentials",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    login(request, user)

    return Response(
        {
            "detail": "Logged in",
        },
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request):

    logout(request)

    return Response(
        {
            "detail": "Logged out",
        },
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me_view(request):

    return Response(
        {
            "id": request.user.id,
            "username": request.user.username,
            "email": request.user.email,
        }
    )