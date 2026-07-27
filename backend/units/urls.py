from django.urls import path

from .api import UnitListAPI

urlpatterns = [
    path("", UnitListAPI.as_view(), name="units"),
]
