from django.urls import path

from . import views

urlpatterns = [
    path("", views.recipes, name="recipes"),
    path("create/", views.recipe_create, name="recipe_create"),
    path("<int:recipe_id>/copy/", views.recipe_copy, name="recipe_copy"),
    path("<int:recipe_id>/", views.recipe_edit, name="recipe_edit"),
    path("<int:recipe_id>/delete/", views.recipe_delete, name="recipe_delete"),
    path(
        "<int:recipe_id>/add-ingredient/",
        views.add_recipe_ingredient,
        name="add_recipe_ingredient",
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
    path(
        "meal/<str:meal_id>/<str:meal_name>/<str:meal_date>/add/",
        views.add_recipes_to_meal_direct,
        name="add_recipes_to_meal_direct",
    ),
    path(
        "ingredient/<int:ingredient_id>/delete/",
        views.ingredient_delete,
        name="ingredient_delete",
    ),
]
