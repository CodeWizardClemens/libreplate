from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from foods.serializers import FoodSerializer
from integrations import usda_client
from integrations.usda_client import USDAError

from .serializers import (
    USDAFoodSearchResponseSerializer,
    USDAFoodSearchSerializer,
    USDASaveSerializer,
)


class USDASearchAPIView(APIView):
    authentication_classes = [SessionAuthentication]

    permission_classes = [IsAuthenticated]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="term",
                type=str,
                location=OpenApiParameter.QUERY,
                required=True,
                description="Search term for USDA foods.",
            ),
        ],
        responses={
            200: USDAFoodSearchResponseSerializer,
            400: {"description": "Invalid search parameters or USDA error."},
        },
    )
    def get(self, request):

        serializer = USDAFoodSearchSerializer(
            data=request.query_params,
        )

        serializer.is_valid(raise_exception=True)

        try:
            foods = usda_client.search(
                **serializer.validated_data,
            )

        except USDAError as exc:
            return Response(
                {
                    "error": str(exc),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "foods": FoodSerializer(
                    foods,
                    many=True,
                ).data,
            }
        )


class USDASaveAPIView(APIView):
    authentication_classes = [SessionAuthentication]

    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=USDASaveSerializer,
        responses={
            201: {"description": "Food successfully saved."},
            400: {"description": "Invalid FDC ID or USDA error."},
        },
    )
    def post(self, request):

        serializer = USDASaveSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        try:
            food = usda_client.save_by_id(
                serializer.validated_data["fdc_id"],
                user=request.user,
            )

        except USDAError as exc:
            return Response(
                {"error": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            FoodSerializer(food).data,
            status=status.HTTP_201_CREATED,
        )
