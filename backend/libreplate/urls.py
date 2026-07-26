from django.conf import settings
from django.http import FileResponse
from django.urls import include, path, re_path
from django.views.static import serve

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)


def react_app(request):
    return FileResponse(
        (settings.FRONTEND_DIST / "index.html").open("rb")
    )


urlpatterns = [
    # =========================
    # API routes
    # =========================

    path("api/accounts/", include("accounts.api_urls")),
    path("api/foods/", include("foods.api_urls")),
    path("api/groceries/", include("groceries.api_urls")),
    path("api/recipes/", include("recipes.urls")),
    path("api/meals/", include("meals.urls")),
    path("api/nutrients/", include("nutrients.urls")),
    path("api/integrations/", include("integrations.urls")),
]


# =========================
# API documentation
# Only enabled in development
# =========================

if settings.DEBUG:
    urlpatterns += [
        path(
            "api/schema/",
            SpectacularAPIView.as_view(),
            name="schema",
        ),

        path(
            "api/docs/",
            SpectacularSwaggerView.as_view(
                url_name="schema"
            ),
            name="swagger-ui",
        ),

        path(
            "api/redoc/",
            SpectacularRedocView.as_view(
                url_name="schema"
            ),
            name="redoc",
        ),
    ]


# =========================
# React frontend assets
# =========================

urlpatterns += [
    re_path(
        r"^assets/(?P<path>.*)$",
        serve,
        {
            "document_root": settings.FRONTEND_DIST / "assets",
        },
    ),

    re_path(
        r"^(?P<path>[^/]+\.(?:png|jpg|jpeg|svg|ico|webp|gif|txt))$",
        serve,
        {
            "document_root": settings.FRONTEND_DIST,
        },
    ),

    re_path(
        r"^favicon\.ico$",
        serve,
        {
            "document_root": settings.FRONTEND_DIST,
            "path": "favicon.ico",
        },
    ),

    # React SPA fallback
    re_path(
        r"^(?!api/).*",
        react_app,
    ),
]