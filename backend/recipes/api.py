
from rest_framework import status, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .models import Recipe, RecipeIngredient
from .serializers import RecipeSerializer
from .models import Recipe
from django.utils import timezone
from rest_framework.response import Response

class RecipeViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = RecipeSerializer

    def get_queryset(self):
        return Recipe.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"])
    def toggle_favorite(self, request, pk=None):
        recipe = self.get_object()

        recipe.is_favorite = not recipe.is_favorite
        recipe.save(update_fields=["is_favorite", "updated_at"])

        return Response({
            "id": recipe.id,
            "is_favorite": recipe.is_favorite,
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def toggle_pin(self, request, pk=None):
        recipe = self.get_object()

        recipe.is_pinned = not recipe.is_pinned
        recipe.save(update_fields=["is_pinned", "updated_at"])

        return Response({
            "id": recipe.id,
            "is_pinned": recipe.is_pinned,
        }, status=status.HTTP_200_OK)


    @action(detail=True, methods=["post"])
    def copy(self, request, pk=None):
        recipe = self.get_object()

        new_name = request.data.get("name")

        if not new_name:
            return Response(
                {"name": "This field is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Copy recipe fields
        new_recipe = Recipe.objects.create(
            user=request.user,
            name=new_name,
            summary=recipe.summary,
            description=recipe.description,
            instructions=recipe.instructions,
            cooking_time=recipe.cooking_time,
            portions=recipe.portions,
            is_favorite=False,
            is_pinned=False,
            last_used_at=timezone.now(),
        )

        # Copy ingredients
        for ingredient in recipe.ingredients.all():
            RecipeIngredient.objects.create(
                recipe=new_recipe,
                food=ingredient.food,
                serving_amount=ingredient.serving_amount,
                # add any other RecipeIngredient fields here
            )

        # Copy tags
        new_recipe.tags.set(recipe.tags.all())

        serializer = self.get_serializer(new_recipe)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )