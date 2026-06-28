from django.urls import path
from . import views

urlpatterns = [
    path("", views.recipes, name="recipes"),
    path("create/", views.recipe_create, name="recipe_create"),
    path("<int:recipe_id>/", views.recipe_edit, name="recipe_edit"),
    path("<int:recipe_id>/delete/", views.recipe_delete, name="recipe_delete"),

    path(
        "<int:recipe_id>/add-ingredient/",
        views.add_recipe_ingredient,
        name="add_recipe_ingredient",
    ),
    path(
        "ingredient/<int:ingredient_id>/delete/",
        views.delete_recipe_ingredient,
        name="delete_recipe_ingredient",
    ),
    path(
        "<int:recipe_id>/nutrition/",
        views.recipe_nutrition_ajax,
        name="recipe_nutrition_ajax",
    ),
    path(
        "<int:recipe_id>/add-to-diary/",
        views.add_recipe_to_diary,
        name="add_recipe_to_diary",
    ),
]