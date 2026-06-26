# foods/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.foods, name="foods"),
    path("create/", views.create_food, name="create_food"),
    path("<int:pk>/edit/", views.edit_food, name="edit_food"),
    path("<int:pk>/delete/", views.delete_food, name="delete_food"),
    path("search/", views.openfood_search, name="openfood_search"),
    path("import/", views.import_openfood, name="import_openfood"),
    path("select_meal/", views.select_meal, name="select_meal"),
    path(
        "meals/<int:meal_id>/add_foods/",
        views.add_foods_to_meal,
        name="add_foods_to_meal",
    ),
    path(
        "meal/<str:meal_id>/add/",
        views.add_foods_to_meal_direct,
        name="add_foods_to_meal_direct",
    ),
]
