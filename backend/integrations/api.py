from integrations.usda import USDAError, save_by_id, search
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import USDAFoodSearchSerializer, USDASaveSerializer


class USDASearchAPIView(APIView):

    authentication_classes = [
        SessionAuthentication
    ]

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        serializer = USDAFoodSearchSerializer(
            data=request.query_params
        )

        serializer.is_valid(
            raise_exception=True
        )

        try:
            result = search(
                user=request.user,
                **serializer.validated_data,
            )

        except USDAError as exc:
            return Response(
                {
                    "error": str(exc)
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


        foods = [
            {
                "name": food.name,
                "brand": food.brand,
                "fdc_id": food.usda_fdc_id,
                "description": food.description,
            }
            for food in result["foods"]
        ]


        return Response(
            {
                "foods": foods,
                "pagination": result["pagination"],
            }
        )

class USDASaveAPIView(APIView):

    authentication_classes = [
        SessionAuthentication
    ]

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request):

        serializer = USDASaveSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )


        try:
            food = save_by_id(
                serializer.validated_data["fdc_id"],
                user=request.user,
            )

        except USDAError as exc:
            return Response(
                {
                    "error": str(exc)
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


        return Response(
            {
                "id": food.id,
                "name": food.name,
            },
            status=status.HTTP_201_CREATED,
        )