from django.urls import path

from .api import (
    RecipeViewSet,
    RecipeTagViewSet,
    RecipeIngredientViewSet,
    RecipePictureViewSet,
)


recipe_list = RecipeViewSet.as_view(
    {
        "get": "list",
        "post": "create",
    }
)


recipe_detail = RecipeViewSet.as_view(
    {
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy",
    }
)


toggle_favorite = RecipeViewSet.as_view(
    {
        "post": "toggle_favorite",
    }
)


toggle_pin = RecipeViewSet.as_view(
    {
        "post": "toggle_pin",
    }
)


recipe_copy = RecipeViewSet.as_view(
    {
        "post": "copy",
    }
)


tag_list = RecipeTagViewSet.as_view(
    {
        "get": "list",
        "post": "create",
    }
)


tag_detail = RecipeTagViewSet.as_view(
    {
        "delete": "destroy",
    }
)


recipe_ingredients = RecipeIngredientViewSet.as_view(
    {
        "get": "list",
        "post": "create",
    }
)


recipe_ingredient_detail = RecipeIngredientViewSet.as_view(
    {
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy",
    }
)


recipe_picture = RecipePictureViewSet.as_view(
    {
        "get": "retrieve",
        "post": "create",
        "delete": "destroy",
    }
)


urlpatterns = [

    path(
        "",
        recipe_list,
    ),


    # Tags

    path(
        "tags/",
        tag_list,
    ),

    path(
        "tags/<int:pk>/delete/",
        tag_detail,
    ),



    # Recipes

    path(
        "<int:pk>/",
        recipe_detail,
    ),

    path(
        "<int:pk>/toggle-favorite/",
        toggle_favorite,
    ),

    path(
        "<int:pk>/toggle-pin/",
        toggle_pin,
    ),

    path(
        "<int:pk>/copy/",
        recipe_copy,
    ),



    # Ingredients

    path(
        "<int:pk>/ingredients/",
        recipe_ingredients,
    ),

    path(
        "<int:pk>/ingredients/<int:ingredient_pk>/",
        recipe_ingredient_detail,
    ),



    # Picture

    path(
        "<int:pk>/picture/",
        recipe_picture,
    ),
]