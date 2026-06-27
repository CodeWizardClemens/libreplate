from django.urls import path
from . import views

urlpatterns = [
    path("", views.scripts, name="scripts"),
    path("create/", views.script_create, name="script_create"),
    path("<int:script_id>/edit/", views.edit_script, name="edit_script"),
    path("<int:script_id>/run/", views.run_script, name="run_script"),
    path("<int:script_id>/add-step/", views.add_step, name="add_step"),
    path("step/<int:step_id>/update/", views.update_step, name="update_step"),
    path("step/<int:step_id>/delete/", views.delete_step, name="delete_step"),
    path(
        "step/<int:step_id>/select-food/<int:food_id>/",
        views.select_food_for_step,
        name="select_food_for_step",
    ),
]
