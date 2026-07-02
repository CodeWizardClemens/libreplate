# foods/urls.py
from django.urls import path

from . import views
from .views import FoodView

urlpatterns = [
    path("", FoodView.as_view(), name="foods"),
    path("create/", views.create_food, name="create_food"),
    path("<int:pk>/edit/", views.edit_food, name="edit_food"),
    path("<int:pk>/delete/", views.delete_food, name="delete_food"),
    path(
        "usda/<int:fdc_id>/import/",
        views.import_usda_food_view,
        name="import_usda_food",
    ),
    path("select_meal/", views.select_meal, name="select_meal"),
    path(
        "meals/<int:meal_id>/add_foods/",
        views.add_foods_to_meal,
        name="add_foods_to_meal",
    ),
    path(
        "meal/<str:meal_id>/<str:meal_name>/<str:meal_date>/add/",
        views.add_foods_to_meal_direct,
        name="add_foods_to_meal_direct",
    ),
    path(
        "add-to-recipe/<int:recipe_id>/",
        views.add_foods_to_recipe_direct,
        name="add_foods_to_recipe_direct",
    ),
    path(
        "<int:pk>/food-toggle-favorite/",
        views.food_toggle_favorite,
        name="food_toggle_favorite",
    ),
]
