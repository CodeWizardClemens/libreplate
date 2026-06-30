from django.urls import path

from . import views

urlpatterns = [
    path("", views.automations, name="automations"),
    path("create/", views.automation_create, name="automation_create"),
    path("<int:automation_id>/edit/", views.edit_automation, name="edit_automation"),
    path("<int:automation_id>/run/", views.run_automation, name="run_automation"),
    path("<int:automation_id>/delete/", views.delete_automation, name="delete_automation"),

]
