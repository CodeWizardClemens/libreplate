from django.conf import settings
from django.http import FileResponse
from django.urls import include, path, re_path
from django.views.static import serve


def react_app(request):
    return FileResponse(
        (settings.FRONTEND_DIST / "index.html").open("rb")
    )


urlpatterns = [
    # API routes
    path("api/accounts/", include("accounts.api_urls")),
    path("api/foods/", include("foods.api_urls")),
    path("api/groceries/", include("groceries.api_urls")),
    path("api/recipes/", include("recipes.urls")),
    path("api/meals/", include("meals.urls")),
    path("api/nutrients/", include("nutrients.urls")),

    re_path(
        r"^assets/(?P<path>.*)$",
        serve,
        {
            "document_root": settings.FRONTEND_DIST / "assets",
        },
    ),

    # Frontend root static files
    # (logo.png, favicon.ico, robots.txt, etc.)
    re_path(
        r"^(?P<path>[^/]+\.(?:png|jpg|jpeg|svg|ico|webp|gif|txt))$",
        serve,
        {
            "document_root": settings.FRONTEND_DIST,
        },
    ),

    # React SPA fallback
    re_path(
        r"^(?!api/).*",
        react_app,
    ),
]