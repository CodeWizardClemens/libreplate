from django.urls import path
from . import views

urlpatterns = [
    path("", views.settings_page, name="settings"),
    path("api/sidebar/toggle/", views.toggle_sidebar, name="toggle_sidebar"),
    path("default_meals/", views.default_meals, name="default_meals"),
    path(
        "default_meals/create/", views.create_default_meal, name="create_default_meal"
    ),
    path(
        "default_meals/<int:pk>/edit/",
        views.edit_default_meal,
        name="edit_default_meal",
    ),
    path(
        "default_meals/<int:pk>/delete/",
        views.delete_default_meal,
        name="delete_default_meal",
    ),
    path(
        "default_meals/default_meals/reorder/",
        views.reorder_default_meals,
        name="reorder_default_meals",
    ),
    path(
        "api_configuration",
        views.api_configuration,
        name="api_configuration",
    ),
]
