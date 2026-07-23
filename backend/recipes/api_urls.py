from django.urls import path

from .api import RecipeViewSet, RecipeTagViewSet


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


# Tag endpoints
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


urlpatterns = [
    path("", recipe_list),

    # Tags
    path("tags/", tag_list),
    path("tags/<int:pk>/delete/", tag_detail),

    # Recipes
    path("<int:pk>/", recipe_detail),
    path("<int:pk>/toggle-favorite/", toggle_favorite),
    path("<int:pk>/toggle-pin/", toggle_pin),
    path("<int:pk>/copy/", recipe_copy),
]