# foods/urls.py
from django.urls import path

from . import views
from .views import FoodView

urlpatterns = [
    path("", FoodView.as_view(), name="foods"),
    path("create/", views.food_create, name="food_create"),
    path("<int:pk>/edit/", views.food_edit, name="food_edit"),
    path("<int:food_id>/delete/", views.food_delete, name="food_delete"),
    path("<int:food_id>/favorite/", views.toggle_favorite, name="food_toggle_favorite"),

    path(
        "usda/<int:fdc_id>/import/",
        views.import_usda_food_view,
        name="import_usda_food",
    ),
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
        "<int:food_id>/tags/modal/",
        views.tags_modal,
        name="tags_modal",
    ),
    path(
        "<int:food_id>/tags/save/",
        views.tags_save,
        name="tags_save",
    ),
]
