from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.default_page),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/profile/", views.profile, name="profile"),
    path("settings/units/", include("units.urls")),
    path("foods/", include("foods.urls")),
    path("nutrients/", include("nutrients.urls")),
    path("diary/", include("diary.urls")),
    path("groceries/", include("groceries.urls")),
    path("recipes/", include("recipes.urls")),
    path("body-metrics/", include("body_metrics.urls")),
    path("goals/", include("goals.urls")),
    path("settings/", include("settings.urls")),
    path("automations/", include("automations.urls")),
    path("user_statistics/", include("user_statistics.urls")),
    path("api/", include("groceries.api_urls")),
]
