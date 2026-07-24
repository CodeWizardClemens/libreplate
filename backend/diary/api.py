from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Meal
from .serializers import MealSerializer


class MealViewSet(ModelViewSet):
    serializer_class = MealSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self):
        return (
            Meal.objects
            .filter(
                user=self.request.user
            )
            .prefetch_related(
                "meal_foods__food__food_nutrients__nutrient"
            )
        )

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )