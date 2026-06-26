from django.urls import path
from . import views

urlpatterns = [
    path("", views.goals_page, name="goals"),
    path("group/add/", views.add_group, name="add_goal_group"),
    path("group/<int:pk>/delete/", views.delete_group, name="delete_goal_group"),
    path("group/<int:pk>/rename/", views.rename_group, name="rename_goal_group"),
    path("group/<int:pk>/add-item/", views.add_goal_item, name="add_goal_item"),
    path(
        "group/<int:pk>/add-item/post/",
        views.add_goal_item_post,
        name="add_goal_item_post",
    ),
]
