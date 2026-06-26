# body_metrics/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.body_metrics, name="body_metrics"),
    path("create/", views.create_body_metric, name="create_body_metric"),
    path("<int:pk>/edit/", views.edit_body_metric, name="edit_body_metric"),
    path("<int:pk>/delete/", views.delete_body_metric, name="delete_body_metric"),
    path(
        "body-metrics/reorder/", views.reorder_body_metrics, name="reorder_body_metrics"
    ),
    path(
        "<int:pk>/toggle-visibility/",
        views.toggle_body_metric_visibility,
        name="toggle_body_metric_visibility",
    ),
]
