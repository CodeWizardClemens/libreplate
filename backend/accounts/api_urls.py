from django.urls import path

from .api import login_view

urlpatterns = [
    path(
        "login/",
        login_view,
        name="login",
    ),

]