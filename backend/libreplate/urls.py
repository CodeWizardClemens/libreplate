from django.conf import settings
from django.conf.urls.static import static
from django.http import FileResponse
from django.urls import include, path, re_path
from django.views.static import serve


def react_app(request):
    return FileResponse(
        (settings.FRONTEND_DIST / "index.html").open("rb")
    )


urlpatterns = [
    path("api/accounts/", include("accounts.api_urls")),
    path("api/foods/", include("foods.api_urls")),
    path("api/groceries/", include("groceries.api_urls")),
    path("api/recipes/", include("recipes.urls")),
    path("api/meals/", include("meals.urls")),
    path("api/nutrients/", include("nutrients.urls")),

    # React static assets
    re_path(
        r"^assets/(?P<path>.*)$",
        serve,
        {
            "document_root": settings.FRONTEND_DIST / "assets",
        },
    ),

    # React SPA
    re_path(
        r"^(?!api/).*",
        react_app,
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )