from django.urls import path

from .api import GroceryListViewSet, GroceryListFoodViewSet

grocery_list = GroceryListViewSet.as_view({
    "get": "list",
    "post": "create",
})

grocery_detail = GroceryListViewSet.as_view({
    "get": "retrieve",
    "delete": "destroy",
})

item_list = GroceryListFoodViewSet.as_view({
    "get": "list",
    "post": "create",
})

item_detail = GroceryListFoodViewSet.as_view({
    "patch": "partial_update",
    "delete": "destroy",
})

item_toggle = GroceryListFoodViewSet.as_view({
    "post": "toggle",
})

urlpatterns = [
    path("groceries/", grocery_list),
    path("groceries/<int:pk>/", grocery_detail),
    path("groceries/<int:grocery_pk>/items/", item_list),
    path("groceries/<int:grocery_pk>/items/<int:pk>/", item_detail),
    path("groceries/<int:grocery_pk>/items/<int:pk>/toggle/", item_toggle),
]