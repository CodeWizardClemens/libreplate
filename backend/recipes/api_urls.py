from django.urls import path

from .api import RecipeViewSet


recipe_list = RecipeViewSet.as_view({
    "get": "list",
    "post": "create",
})

recipe_detail = RecipeViewSet.as_view({
    "get": "retrieve",
    "put": "update",
    "patch": "partial_update",
    "delete": "destroy",
})

toggle_favorite = RecipeViewSet.as_view({
    "post": "toggle_favorite",
})

toggle_pin = RecipeViewSet.as_view({
    "post": "toggle_pin",
})

recipe_copy = RecipeViewSet.as_view({
    "post": "copy",
})

urlpatterns = [
    path("", recipe_list),
    path("<int:pk>/", recipe_detail),

    path("<int:pk>/toggle-favorite/", toggle_favorite),
    path("<int:pk>/toggle-pin/", toggle_pin),

    path("<int:pk>/copy/", recipe_copy),
]