from django.urls import path

from . import views

urlpatterns = [
    path("", views.meal_plans, name="meal_plans"),
    path("create/", views.meal_plan_create, name="meal_plan_create"),
    path("<int:meal_plan_id>/copy/", views.meal_plan_copy, name="meal_plan_copy"),
    path("<int:meal_plan_id>/", views.meal_plan_edit, name="meal_plan_edit"),
    path("<int:meal_plan_id>/delete/", views.meal_plan_delete, name="meal_plan_delete"),
    path("<int:pk>/title/", views.meal_plan_title, name="meal_plan_title"),
    path("<int:pk>/rename-form/", views.meal_plan_rename_form, name="meal_plan_rename_form"),
    path("<int:pk>/rename/", views.meal_plan_rename, name="meal_plan_rename"),
]
