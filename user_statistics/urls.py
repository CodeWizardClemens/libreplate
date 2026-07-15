from django.urls import path

from . import views

urlpatterns = [
    path("", views.graph_list, name="graph_list"),
    path("new/", views.graph_create, name="graph_create"),
    path("<uuid:pk>/edit/", views.graph_edit, name="graph_edit"),
    path("<uuid:pk>/delete/", views.graph_delete, name="graph_delete"),
    path(
    "<uuid:pk>/data/",
    views.graph_data,
    name="graph_data",
),
]