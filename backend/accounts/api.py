from django.contrib.auth import authenticate, login

from rest_framework.decorators import (
    api_view,
    permission_classes,
)

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status


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