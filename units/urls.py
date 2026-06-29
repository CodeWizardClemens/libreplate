# units/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path("", views.units, name="units"),
    path("create/", views.create_unit, name="create_unit"),
    path("<int:pk>/edit/", views.edit_unit, name="edit_unit"),
    path("<int:pk>/delete/", views.delete_unit, name="delete_unit"),
]
