from django.urls import path
from . import views

urlpatterns = [
    path("", views.diary_day, name="diary_today"),
    path("<str:date>/", views.diary_day, name="diary_day"),
    path("<str:date>/add-meal/", views.add_meal, name="add_meal"),
    path("meal/<str:meal_id>/delete/", views.delete_meal, name="delete_meal"),
    path(
        "meal/<str:meal_id>/add-food/", views.add_food_to_meal, name="add_food_to_meal"
    ),
    path(
        "meal-food/<int:meal_food_id>/delete/",
        views.delete_meal_food,
        name="delete_meal_food",
    ),
    path("meal/<str:meal_id>/note/", views.update_note, name="update_note"),
    path("body-metrics/save/", views.save_body_metric, name="save_body_metric"),
    path(
        "meal-food/update/",
        views.update_meal_food,
        name="update_meal_food",
    ),
]
