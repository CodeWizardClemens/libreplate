"""libreplate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
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
    path("scripts/", include("scripts.urls")),
    path("user_statistics/", include("user_statistics.urls")),
]
