from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    # Web views
    path("", views.default_page),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/profile/", views.profile, name="profile"),
    path("diary/", include("diary.urls")),
    path("foods/", include("foods.urls")),
    path("goals/", include("goals.urls")),
    path("groceries/", include("groceries.urls")),
    path("meal_plans/", include("meal_plans.urls")),
    path("recipes/", include("recipes.urls")),
    path("user-statistics/", include("user_statistics.urls")),
    path("settings/", include("settings.urls")),
    path("settings/body-metrics/", include("body_metrics.urls")),
    path("settings/default_meals/", include("default_meals.urls")),
    path("settings/nutrients/", include("nutrients.urls")),
    path("settings/units/", include("units.urls")),

    # API
    path("api/accounts/", include("accounts.api_urls")),
    path("api/groceries/", include("groceries.api_urls")),
    path("api/recipes/", include("recipes.api_urls")),

]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )