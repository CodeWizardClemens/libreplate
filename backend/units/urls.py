# units/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path("", views.units, name="units"),
    path("create/", views.unit_form, name="create_unit"),
    path("<uuid:pk>/edit/", views.unit_form, name="edit_unit"),
    path("<uuid:pk>/delete/", views.unit_delete, name="delete_unit"),
]
