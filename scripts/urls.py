from django.urls import path

from . import views

urlpatterns = [
    path("", views.scripts, name="scripts"),
    path("create/", views.script_create, name="script_create"),
    path("<int:script_id>/edit/", views.edit_script, name="edit_script"),
    path("<int:script_id>/run/", views.run_script, name="run_script"),
    path("<int:script_id>/delete/", views.delete_script, name="delete_script"),

]
