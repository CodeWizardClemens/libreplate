from django.urls import path

from .api import (
    USDASearchAPIView,
    USDASaveAPIView,
)


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