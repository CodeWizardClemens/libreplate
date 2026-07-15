from django.urls import path

from . import views

urlpatterns = [
    path("", views.settings_page, name="settings"),
    path("appearance", views.appearance, name="appearance"),

    path("api/sidebar/toggle/", views.toggle_sidebar, name="toggle_sidebar"),
]
