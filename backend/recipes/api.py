from django.utils import timezone

from rest_framework import status, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import (
    Recipe,
    RecipeIngredient,
    RecipeTag,
)

from .serializers import (
    RecipeSerializer,
    RecipeTagSerializer,
    RecipeIngredientSerializer,
)



class RecipeViewSet(viewsets.ModelViewSet):

    authentication_classes = [
        SessionAuthentication
    ]

    permission_classes = [
        IsAuthenticated
    ]

    serializer_class = RecipeSerializer


    def get_queryset(self):

        return Recipe.objects.filter(
            user=self.request.user
        )


    def perform_create(self, serializer):

        serializer.save(
            user=self.request.user
        )


    @action(
        detail=True,
        methods=["post"]
    )
    def toggle_favorite(self, request, pk=None):

        recipe = self.get_object()

        recipe.is_favorite = not recipe.is_favorite

        recipe.save(
            update_fields=[
                "is_favorite",
                "updated_at",
            ]
        )

        return Response(
            {
                "id": recipe.id,
                "is_favorite": recipe.is_favorite,
            }
        )


    @action(
        detail=True,
        methods=["post"]
    )
    def toggle_pin(self, request, pk=None):

        recipe = self.get_object()

        recipe.is_pinned = not recipe.is_pinned

        recipe.save(
            update_fields=[
                "is_pinned",
                "updated_at",
            ]
        )

        return Response(
            {
                "id": recipe.id,
                "is_pinned": recipe.is_pinned,
            }
        )


    @action(
        detail=True,
        methods=["post"]
    )
    def copy(self, request, pk=None):

        recipe = self.get_object()

        new_name = request.data.get("name")


        if not new_name:

            return Response(
                {
                    "name": "This field is required."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


        new_recipe = Recipe.objects.create(
            user=request.user,
            name=new_name,
            summary=recipe.summary,
            description=recipe.description,
            instructions=recipe.instructions,
            cooking_time=recipe.cooking_time,
            portions=recipe.portions,
            last_used_at=timezone.now(),
        )


        for ingredient in recipe.ingredients.all():

            RecipeIngredient.objects.create(
                recipe=new_recipe,
                food=ingredient.food,
                default_servings=ingredient.default_servings,
                serving_amount=ingredient.serving_amount,
                min_servings=ingredient.min_servings,
                max_servings=ingredient.max_servings,
                order=ingredient.order,
            )


        new_recipe.tags.set(
            recipe.tags.all()
        )


        return Response(
            self.get_serializer(new_recipe).data,
            status=status.HTTP_201_CREATED,
        )





class RecipeTagViewSet(viewsets.ModelViewSet):

    authentication_classes = [
        SessionAuthentication
    ]

    permission_classes = [
        IsAuthenticated
    ]

    serializer_class = RecipeTagSerializer


    def get_queryset(self):

        return RecipeTag.objects.filter(
            user=self.request.user
        )


    def perform_create(self, serializer):

        serializer.save(
            user=self.request.user
        )





class RecipeIngredientViewSet(viewsets.ModelViewSet):

    authentication_classes = [
        SessionAuthentication
    ]

    permission_classes = [
        IsAuthenticated
    ]

    serializer_class = RecipeIngredientSerializer


    def get_recipe(self):

        return Recipe.objects.get(
            id=self.kwargs["pk"],
            user=self.request.user,
        )


    def get_queryset(self):

        recipe = self.get_recipe()

        return RecipeIngredient.objects.filter(
            recipe=recipe
        ).select_related(
            "food"
        )


    def perform_create(self, serializer):

        serializer.save(
            recipe=self.get_recipe()
        )