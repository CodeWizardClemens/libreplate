from django.urls import path

from . import views

urlpatterns = [
    path("toggle-dark-mode/", views.toggle_dark_mode, name="toggle_dark_mode"),
    path(
        "preferences/theme-color/", views.update_theme_color, name="update_theme_color"
    ),
]
