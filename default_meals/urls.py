from django.urls import path

from . import views

urlpatterns = [
    path("", views.default_meals, name="default_meals"),
    path(
        "create/", views.create_default_meal, name="create_default_meal"
    ),
    path(
        "<int:pk>/edit/",
        views.edit_default_meal,
        name="edit_default_meal",
    ),
    path(
        "<int:pk>/delete/",
        views.delete_default_meal,
        name="delete_default_meal",
    ),
    path(
        "default_meals/reorder/",
        views.reorder_default_meals,
        name="reorder_default_meals",
    ),
]