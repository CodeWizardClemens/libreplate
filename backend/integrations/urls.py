from django.urls import path

from .api import USDASaveAPIView, USDASearchAPIView

urlpatterns = [
    path(
        "usda/search/",
        USDASearchAPIView.as_view(),
    ),
    path(
        "usda/save/",
        USDASaveAPIView.as_view(),
    ),
]
