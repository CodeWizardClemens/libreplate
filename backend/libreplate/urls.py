from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    # API
    path("api/accounts/", include("accounts.api_urls")),
    path("api/foods/", include("foods.api_urls")),
    path("api/groceries/", include("groceries.api_urls")),
    path("api/recipes/", include("recipes.urls")),
    path("api/meals/", include("meals.urls")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )

    urlpatterns += [
        path("", views.default_page),
        path("accounts/", include("accounts.urls")),
        path("accounts/", include("django.contrib.auth.urls")),
        path("accounts/profile/", views.profile, name="profile"),
    ]