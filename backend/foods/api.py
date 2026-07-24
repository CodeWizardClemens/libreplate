from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Food
from .serializers import FoodSerializer


class FoodViewSet(ModelViewSet):
    serializer_class = FoodSerializer
    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):
        return (
            Food.objects
            .filter(
                user=self.request.user
            )
            .prefetch_related(
                "food_nutrients__nutrient"
            )
        )

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )