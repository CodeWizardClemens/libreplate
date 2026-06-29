from django.urls import path

from . import views

urlpatterns = [
    path("", views.goals_page, name="goals"),
    path("create/", views.goal_group_create, name="goal_group_create"),
    path("<int:pk>/", views.goal_group_edit, name="goal_group_edit"),
    path("<int:pk>/delete/", views.goal_group_delete, name="goal_group_delete"),
]
