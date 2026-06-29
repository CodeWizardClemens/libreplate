from django.urls import path

from . import views

urlpatterns = [
    path("", views.user_statistics, name="user_statistics"),
]
