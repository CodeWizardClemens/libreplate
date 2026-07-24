from django.urls import path

from .api import MealViewSet


urlpatterns = [
    path(
        "",
        MealViewSet.as_view({
            "get": "list",
            "post": "create",
        }),
        name="meal-list",
    ),
    path(
        "<int:pk>/",
        MealViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy",
        }),
        name="meal-detail",
    ),
]