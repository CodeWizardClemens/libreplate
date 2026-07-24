from django.urls import path

from .api import FoodViewSet


food_list = FoodViewSet.as_view(
    {
        "get": "list",
        "post": "create",
    }
)


food_detail = FoodViewSet.as_view(
    {
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy",
    }
)


urlpatterns = [
    path(
        "",
        food_list,
        name="food-list",
    ),

    path(
        "<int:pk>/",
        food_detail,
        name="food-detail",
    ),
]