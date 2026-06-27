from django.urls import path
from . import views

urlpatterns = [
    path("", views.nutrients, name="nutrients"),
    path("create/", views.create_nutrient, name="create_nutrient"),
    path("<int:pk>/edit/", views.edit_nutrient, name="edit_nutrient"),
    path("<int:pk>/delete/", views.delete_nutrient, name="delete_nutrient"),
    path("nutrients/reorder/", views.reorder_nutrients, name="reorder_nutrients"),
]
