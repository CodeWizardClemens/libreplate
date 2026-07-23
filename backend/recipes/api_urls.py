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

urlpatterns = [
    path("", recipe_list),
    path("<int:pk>/", recipe_detail),
]