from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import GroceryList, GroceryListFood
from .serializers import (
    GroceryListSerializer,
    GroceryListFoodSerializer,
)
from .services import generate_grocery_items


class GroceryListViewSet(viewsets.ModelViewSet):
    serializer_class = GroceryListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return GroceryList.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        grocery = serializer.save(user=self.request.user)

        if grocery.generate_from_diary:
            generate_grocery_items(grocery)


class GroceryListFoodViewSet(viewsets.ModelViewSet):
    serializer_class = GroceryListFoodSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return GroceryListFood.objects.filter(
            grocery_list__user=self.request.user,
            grocery_list_id=self.kwargs["grocery_pk"],
        )

    def perform_create(self, serializer):
        grocery = get_object_or_404(
            GroceryList,
            pk=self.kwargs["grocery_pk"],
            user=self.request.user,
        )

        serializer.save(grocery_list=grocery)

    @action(detail=True, methods=["post"])
    def toggle(self, request, grocery_pk=None, pk=None):
        item = self.get_object()

        item.has_item = not item.has_item
        item.save(update_fields=["has_item"])

        return Response(
            GroceryListFoodSerializer(item).data,
            status=status.HTTP_200_OK,
        )