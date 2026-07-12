from django.urls import path

from . import views

urlpatterns = [
    path("", views.settings_page, name="settings"),
    path("api/sidebar/toggle/", views.toggle_sidebar, name="toggle_sidebar"),
    path(
        "api_configuration",
        views.api_configuration,
        name="api_configuration",
    ),
]
