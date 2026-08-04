from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Food, FoodTag
from .serializers import FoodSerializer, FoodTagSerializer


class FoodViewSet(ModelViewSet):
    authentication_classes = [
        SessionAuthentication,
    ]

    permission_classes = [
        IsAuthenticated,
    ]

    serializer_class = FoodSerializer

    def get_queryset(self):
        return (
            Food.objects.filter(user=self.request.user)
            .select_related(
                "unit",
            )
            .prefetch_related(
                "tags",
                "food_nutrients__nutrient",
            )
        )

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
        )


class FoodTagViewSet(ModelViewSet):
    authentication_classes = [
        SessionAuthentication,
    ]

    permission_classes = [
        IsAuthenticated,
    ]

    serializer_class = FoodTagSerializer

    def get_queryset(self):
        return FoodTag.objects.filter(
            user=self.request.user,
        )

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
        )
